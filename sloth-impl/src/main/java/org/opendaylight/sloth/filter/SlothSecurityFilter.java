/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.filter;

import org.apache.commons.io.IOUtils;
import org.apache.shiro.SecurityUtils;
import org.opendaylight.aaa.api.shiro.principal.ODLPrincipal;
import org.opendaylight.sloth.exception.ServiceUnavailableException;
import org.opendaylight.sloth.service.SlothServiceLocator;
import org.opendaylight.sloth.utils.GenericResponseWrapper;
import org.opendaylight.sloth.utils.MultiHttpServletRequest;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.CheckPermissionInputBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.CheckPermissionOutput;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.HttpType;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.SlothPermissionService;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.check.permission.input.Principal;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.check.permission.input.PrincipalBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.check.permission.input.Request;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.check.permission.input.RequestBuilder;
import org.opendaylight.yangtools.yang.common.RpcResult;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Objects;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Future;

public class SlothSecurityFilter implements Filter {
    private static final Logger LOG = LoggerFactory.getLogger(SlothSecurityFilter.class);
    private static final String JSON_CONTENT_TYPE = "application/json";
    private final SlothPermissionService slothPermissionService;

    public SlothSecurityFilter() throws ServiceUnavailableException {
        slothPermissionService = SlothServiceLocator.getInstance().getPermissionService();
    }

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        LOG.info("SlothSecurityFilter initialized");
    }

    @Override
    public void doFilter(ServletRequest servletRequest, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        if (servletRequest instanceof HttpServletRequest) {
            long startTime = System.nanoTime();
            HttpServletRequest httpServletRequest = (HttpServletRequest) servletRequest;
            HttpServletRequest multiReadHttpServletRequest =
                    httpServletRequest.getContentType() != null && Objects.equals(httpServletRequest.getContentType(), JSON_CONTENT_TYPE) ?
                            new MultiHttpServletRequest(httpServletRequest) : httpServletRequest;

            Principal principal = getPrincipal((ODLPrincipal) SecurityUtils.getSubject().getPrincipal());
            final Future<RpcResult<CheckPermissionOutput>> rpcResultFuture = slothPermissionService
                    .checkPermission(new CheckPermissionInputBuilder().setPrincipal(principal)
                            .setRequest(getRequest(multiReadHttpServletRequest, null)).build());
            try {
                RpcResult<CheckPermissionOutput> rpcResult = rpcResultFuture.get();
                if (rpcResult.isSuccessful()) {
                    long endTime = System.nanoTime();
                    LOG.info("Permission Checking Time: " + (endTime - startTime) + " nano seconds");
                    LOG.info("SlothSecurityFilter, check permission successful");
                    if (rpcResult.getResult().getStatusCode() / 100 == 2) {
                        if (multiReadHttpServletRequest.getMethod().equals("GET")) {
                            LOG.info("response content type: " + multiReadHttpServletRequest.getContentType());
                            GenericResponseWrapper genericResponseWrapper = new GenericResponseWrapper((HttpServletResponse) response);
                            chain.doFilter(multiReadHttpServletRequest, genericResponseWrapper);
                            final Future<RpcResult<CheckPermissionOutput>> resultFuture = slothPermissionService
                                    .checkPermission(new CheckPermissionInputBuilder().setPrincipal(principal)
                                            .setRequest(getRequest(multiReadHttpServletRequest,
                                                    new String(genericResponseWrapper.getData()))).build());
                            RpcResult<CheckPermissionOutput> result = resultFuture.get();
                            if (result.isSuccessful()) {
                                if (result.getResult().getStatusCode() / 100 == 2) {
                                    response.getOutputStream().write(genericResponseWrapper.getData());
                                } else {
                                    response.getWriter().write(String.format("status code: %s, response: %s",
                                            result.getResult().getStatusCode(), result.getResult().getResponse()));
                                }
                            } else {
                                LOG.warn("SlothSecurityFilter, unknown exception during permission checking, GET check");
                                response.getWriter().write("unknown exception during permission checking, GET check");
                            }
                        } else {
                            chain.doFilter(multiReadHttpServletRequest, response);
                        }
                    } else {
                        response.getWriter().write(String.format("status code: %s, response: %s",
                                rpcResult.getResult().getStatusCode(), rpcResult.getResult().getResponse()));
                    }
                } else {
                    LOG.warn("SlothSecurityFilter, unknown exception during permission checking");
                    response.getWriter().write("unknown exception during permission checking");
                }
            } catch (InterruptedException | ExecutionException e) {
                LOG.error("SlothSecurityFilter, check permission exception: " + e.getMessage());
                response.getWriter().write("exception during check permission: " + e.getMessage());
            }
        } else {
            LOG.warn("not http servletRequest, no permission check");
            chain.doFilter(servletRequest, response);
        }
    }

    @Override
    public void destroy() {
        LOG.info("SlothSecurityFilter destroyed");
    }

    private static Principal getPrincipal(ODLPrincipal odlPrincipal) {
        LOG.info(String.format("create principal, user-id: %s, user-name: %s, domain: %s, roles: %s",
                odlPrincipal.getUserId(), odlPrincipal.getUsername(), odlPrincipal.getDomain(),
                String.join(", ", odlPrincipal.getRoles())));
        ArrayList<String> roles = new ArrayList<>(odlPrincipal.getRoles());
        Collections.sort(roles);
        PrincipalBuilder principalBuilder = new PrincipalBuilder();
        principalBuilder.setUserName(odlPrincipal.getUsername()).setUserId(odlPrincipal.getUserId())
                .setDomain(odlPrincipal.getDomain()).setRoles(roles);
        return principalBuilder.build();
    }

    private static Request getRequest(HttpServletRequest httpServletRequest, String externalJson) {
        LOG.info(String.format("create request, method: %s, request-url: %s, query-string: %s", httpServletRequest.getMethod(),
                httpServletRequest.getRequestURI(), httpServletRequest.getQueryString()));
        RequestBuilder requestBuilder = new RequestBuilder();
        requestBuilder.setMethod(HttpType.valueOf(httpServletRequest.getMethod()))
                .setRequestUrl(httpServletRequest.getRequestURI())
                .setQueryString(httpServletRequest.getQueryString());
        if (externalJson == null || externalJson.isEmpty()) {
            try {
                if (httpServletRequest.getContentType() != null &&
                        Objects.equals(httpServletRequest.getContentType(), JSON_CONTENT_TYPE)) {
                    requestBuilder.setJsonBody(IOUtils.toString(httpServletRequest.getReader()));
                }
            } catch (IOException e) {
                LOG.error("failed to get json body from http servlet request: " + e.getMessage());
            }
        } else {
            requestBuilder.setJsonBody(externalJson);
        }
        return requestBuilder.build();
    }
}

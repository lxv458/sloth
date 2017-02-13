/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.filter;

import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.http.HttpServletRequest;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Future;

import org.apache.shiro.SecurityUtils;
import org.apache.shiro.subject.Subject;
import org.opendaylight.sloth.exception.ServiceUnavailableException;
import org.opendaylight.sloth.service.SlothServiceLocator;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.CheckPermissionInput;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.CheckPermissionInputBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.CheckPermissionOutput;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.SlothPermissionService;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.check.permission.input.PermissionRequestBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.check.permission.input.PermissionUserBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.check.permission.input.permission.user.Roles;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.check.permission.input.permission.user.RolesBuilder;
import org.opendaylight.yangtools.yang.common.RpcResult;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class SlothSecurityFilter implements Filter{
    private static final Logger LOG = LoggerFactory.getLogger(SlothSecurityFilter.class);
    private final SlothPermissionService slothPermissionService;

    public SlothSecurityFilter() throws ServiceUnavailableException {
        slothPermissionService = SlothServiceLocator.getInstance().getPermissionService();
    }

    @Override
    public void init(FilterConfig filterConfig) throws ServletException {
        LOG.info("SlothSecurityFilter initialized");
    }

    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain) throws IOException, ServletException {
        if (request instanceof HttpServletRequest) {
            HttpServletRequest httpServletRequest = (HttpServletRequest) request;
            // TODO: use ODLPrincipal to get username, domain, user id, roles
            /*
             * ODLPrincipal in 0.4.0-Boron is private static class inside TokenAuthRealm
             * ODLPrincipal will be exported as dependency in 0.5.0-Carbon
             * in Carbon version, we can get username, domain, userid, roles
             */
            Subject subject = SecurityUtils.getSubject();
            //ODLPrincipal odlPrincipal = (ODLPrincipal) subject.getPrincipal();
            CheckPermissionInput checkPermissionInput = httpRequestToPermissionInput(subject, httpServletRequest);
            final Future<RpcResult<CheckPermissionOutput>> rpcResultFuture = slothPermissionService.checkPermission(checkPermissionInput);
            try {
                RpcResult<CheckPermissionOutput> rpcResult = rpcResultFuture.get();
                if (rpcResult.isSuccessful()) {
                    LOG.info("SlothSecurityFilter permission result: " + rpcResult.getResult().getPermission());
                    LOG.info("SlothSecurityFilter, check permission successful");
                } else {
                    LOG.warn("SlothSecurityFilter, check permission unsuccessful");
                }
            } catch (InterruptedException | ExecutionException e) {
                e.printStackTrace();
                LOG.error("SlothSecurityFilter, check permission exception");
            }
            chain.doFilter(request, response);
        } else {
            chain.doFilter(request, response);
        }
    }

    @Override
    public void destroy() {
        LOG.info("SlothSecurityFilter destroyed");
    }

    private static CheckPermissionInput httpRequestToPermissionInput(Object principal, HttpServletRequest request) {
        PermissionUserBuilder userBuilder = new PermissionUserBuilder();
        PermissionRequestBuilder requestBuilder = new PermissionRequestBuilder();
        CheckPermissionInputBuilder inputBuilder = new CheckPermissionInputBuilder();

        List<Roles> roles = new ArrayList<>();
        roles.add(new RolesBuilder().setRole("admin").build());
        roles.add(new RolesBuilder().setRole("user").build());
        userBuilder.setUserName("Libin").setUserId("HelloBinge").setDomain("SDN").setRoles(roles);

        // TODO: read json data without altering BufferedReader
        requestBuilder.setMethod(request.getMethod()).setRequestUrl(request.getRequestURI())
                .setQueryString(request.getQueryString());
        return inputBuilder.setPermissionUser(userBuilder.build()).setPermissionRequest(requestBuilder.build()).build();
    }
}

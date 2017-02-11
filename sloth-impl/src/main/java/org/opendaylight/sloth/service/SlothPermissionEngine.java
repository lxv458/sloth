/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
package org.opendaylight.sloth.service;

import org.opendaylight.controller.md.sal.binding.api.DataBroker;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.sloth.rev150105.CheckPermissionInput;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.sloth.rev150105.CheckPermissionOutput;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.sloth.rev150105.CheckPermissionOutputBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.sloth.rev150105.SlothPermissionService;
import org.opendaylight.yangtools.yang.common.RpcResult;
import org.opendaylight.yangtools.yang.common.RpcResultBuilder;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.concurrent.Future;


public class SlothPermissionEngine implements SlothPermissionService {
    private static final Logger LOG = LoggerFactory.getLogger(SlothPermissionEngine.class);

    private final DataBroker dataBroker;

    public SlothPermissionEngine(final DataBroker dataBroker) {
        this.dataBroker = dataBroker;
    }

    @Override
    public Future<RpcResult<CheckPermissionOutput>> checkPermission(CheckPermissionInput input) {
        String requestUrl = input.getRequestUrl();
        String queryString = input.getQueryString();
        String jsonBody = input.getJsonBody();
        LOG.info(requestUrl + queryString + jsonBody);
        CheckPermissionOutputBuilder checkPermissionOutputBuilder = new CheckPermissionOutputBuilder();
        checkPermissionOutputBuilder.setPermission("RequestUrl[" + requestUrl + "], QueryString[" + queryString + "], JSONBody[" + jsonBody + "]");
        return RpcResultBuilder.success(checkPermissionOutputBuilder.build()).buildFuture();
    }
}

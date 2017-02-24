/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.cache;


import com.google.common.base.Preconditions;
import org.opendaylight.controller.md.sal.binding.api.DataBroker;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.CheckPermissionInput;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class SlothReadCacheImpl implements SlothReadCache {
    private static final Logger LOG = LoggerFactory.getLogger(SlothReadCacheImpl.class);

    private final DataBroker dataBroker;
    private final SlothPermissionCache slothPermissionCache;
    private final SlothDomainCache slothDomainCache;

    public SlothReadCacheImpl(DataBroker dataBroker) {
        Preconditions.checkNotNull(dataBroker, "SlothReadCacheImpl initialization failure: empty data broker");
        this.dataBroker = dataBroker;
        slothPermissionCache = new SlothPermissionCache(dataBroker);
        slothDomainCache = new SlothDomainCache(dataBroker);
        LOG.info("SlothReadCacheImpl initialized");
    }

    @Override
    public void close() throws Exception {
        slothPermissionCache.close();
        slothDomainCache.close();
        LOG.info("SlothReadCacheImpl closed");
    }

    @Override
    public boolean checkPermission(CheckPermissionInput input) {
        String roles = "[";
        for (String role : input.getPrincipal().getRoles()) {
            if (roles == "[") {
                roles += role;
            } else {
                roles += ", " + role;
            }
        }
        roles += "]";
        String content = "user-name: " + input.getPrincipal().getUserName() +
                ", user-id: " + input.getPrincipal().getUserId() +
                ", domain: " + input.getPrincipal().getDomain() +
                ", roles: " + roles +
                ", method: " + input.getRequest().getMethod() +
                ", query-string: " + input.getRequest().getQueryString() +
                ", request-url: " + input.getRequest().getRequestUrl() +
                ", json-body: " + input.getRequest().getJsonBody();
        LOG.info(content);
        return true;
    }
}

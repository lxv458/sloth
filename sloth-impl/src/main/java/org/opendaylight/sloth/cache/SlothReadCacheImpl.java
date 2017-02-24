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
import org.opendaylight.sloth.cache.model.SlothCachedRole;
import org.opendaylight.sloth.cache.model.SlothPermissionCheckResult;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.CheckPermissionInput;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;

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
    public SlothPermissionCheckResult checkPermission(CheckPermissionInput input) {
        List<SlothCachedRole> slothCachedRoleList = slothDomainCache.getRelatedSlothCachedRole(input.getPrincipal().getDomain(), input.getPrincipal().getRoles());
        if (slothCachedRoleList != null && slothCachedRoleList.isEmpty()) {
            for (SlothCachedRole role : slothCachedRoleList) {
                List<String> permissionIdList = role.getPermissionId();
                if (permissionIdList != null && permissionIdList.isEmpty()) {
                    for (String permissionId : role.getPermissionId()) {
                        SlothPermissionCheckResult result = slothPermissionCache.getSlothCachedPermission(permissionId).isContradictory(input.getRequest());
                        if (!result.isSuccess()) {
                            return result;
                        }
                    }
                } else {
                    return new SlothPermissionCheckResult(false, "no related permissions for role: " + role.getName());
                }
            }
        } else {
            return new SlothPermissionCheckResult(false, "no related domain/roles in data store");
        }
        return new SlothPermissionCheckResult(true, "");
    }
}

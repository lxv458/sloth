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
import org.opendaylight.sloth.cache.model.SlothCachedPermission;
import org.opendaylight.sloth.cache.model.SlothPolicyCheckResult;
import org.opendaylight.sloth.cache.model.SlothRequest;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.domains.domain.Role;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.CheckPermissionInput;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;

public class SlothReadCacheImpl implements SlothReadCache {
    private static final Logger LOG = LoggerFactory.getLogger(SlothReadCacheImpl.class);

    private final DataBroker dataBroker;
    private final SlothPermissionCache slothPermissionCache;
    private final SlothDomainCache slothDomainCache;
    private final GlobalPolicyCache globalPolicyCache;
    private final LocalPolicyCache localPolicyCache;

    public SlothReadCacheImpl(DataBroker dataBroker) {
        Preconditions.checkNotNull(dataBroker, "SlothReadCacheImpl initialization failure: empty data broker");
        this.dataBroker = dataBroker;
        slothPermissionCache = new SlothPermissionCache(dataBroker);
        slothDomainCache = new SlothDomainCache(dataBroker);
        globalPolicyCache = new GlobalPolicyCache(dataBroker);
        localPolicyCache = new LocalPolicyCache(dataBroker);
        LOG.info("SlothReadCacheImpl initialized");
    }

    @Override
    public void close() throws Exception {
        slothPermissionCache.close();
        slothDomainCache.close();
        globalPolicyCache.close();
        localPolicyCache.close();
        LOG.info("SlothReadCacheImpl closed");
    }

    @Override
    public SlothPolicyCheckResult checkPermission(CheckPermissionInput input) {
        LOG.info("Check permission for input: " + input.getRequest().getRequestUrl() + ", Method: " + input.getRequest().getMethod().getName());
        SlothRequest slothRequest = new SlothRequest(input);
        List<Role> roleList = slothDomainCache.getRelatedRoleList(input.getPrincipal().getDomain(), input.getPrincipal().getRoles());
        if (roleList != null && !roleList.isEmpty()) {
            for (Role role : roleList) {
                List<String> permissionIdList = role.getPermissionId();
                if (permissionIdList != null && !permissionIdList.isEmpty()) {
                    for (String permissionId : role.getPermissionId()) {
                        SlothCachedPermission slothCachedPermission = slothPermissionCache.getSlothCachedPermission(permissionId);
                        if (!slothCachedPermission.isDisabled()) {
                            SlothPolicyCheckResult result = slothCachedPermission.isContradictory(slothRequest);
                            if (!result.isSuccess()) {
                                return result;
                            }
                        }
                    }
                } else {
                    return new SlothPolicyCheckResult(false, "no related permissions for role: " + role.getName());
                }
            }
            return new SlothPolicyCheckResult(true, null);
        } else {
            return new SlothPolicyCheckResult(false, "no related domain/roles. domain: " +
                    input.getPrincipal().getDomain() + "roles: " + String.join(", ", input.getPrincipal().getRoles()));
        }
    }

    @Override
    public SlothPolicyCheckResult policyCheck(CheckPermissionInput input) {
        SlothRequest slothRequest = new SlothRequest(input);
        SlothPolicyCheckResult globalResult = globalPolicyCache.policyCheck(slothRequest);
        if (globalResult.isSuccess() == null) {
            return localPolicyCache.policyCheck(slothRequest);
        } else {
            return globalResult;
        }
    }

    @Override
    public String toString() {
        return "Global Policy Cache\n" + globalPolicyCache.toString() +
                "\nLocal Policy Cache" + localPolicyCache.toString();
    }
}

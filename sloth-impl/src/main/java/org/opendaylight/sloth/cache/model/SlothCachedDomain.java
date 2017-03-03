/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.cache.model;


import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.domains.Domain;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.domains.domain.Role;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SlothCachedDomain {
    private static final Logger LOG = LoggerFactory.getLogger(SlothCachedDomain.class);
    private final Map<String, Role> role;
    private final boolean disabled;

    public SlothCachedDomain(Domain domain) {
        role = new HashMap<>();
        for (Role r : domain.getRole()) {
            role.put(r.getName(), r);
        }
        disabled = domain.isDisabled();
    }

    public List<Role> getRelatedRoleList(List<String> roleNames) {
        LOG.info("get roles for: " + String.join(", ", roleNames));
        List<Role> result = new ArrayList<>();
        for (String roleName : roleNames) {
            if (role.containsKey(roleName)) {
                if (!role.get(roleName).isDisabled()) {
                    result.add(role.get(roleName));
                    LOG.info("add role: " + roleName);
                } else {
                    LOG.warn("role is disabled: " + roleName);
                }
            } else {
                LOG.warn("unable to find role: " + roleName);
            }
        }
        result.sort((r1, r2) -> r2.getPriority() - r1.getPriority());
        return result;
    }

    public boolean isDisabled() {
        return disabled;
    }
}

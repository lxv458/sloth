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

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SlothCachedDomain {
    private final String id;
    private final String name;
    private final Map<String, Role> role;
    private final boolean disabled;

    public SlothCachedDomain(Domain domain) {
        id = domain.getId();
        name = domain.getName();
        role = new HashMap<>();
        for (Role r : domain.getRole()) {
            role.put(r.getName(), r);
        }
        disabled = domain.isDisabled();
    }

    public List<Role> getRelatedRoleList(List<String> roleNames) {
        List<Role> result = new ArrayList<>();
        for (String roleName : roleNames) {
            if (!role.get(roleName).isDisabled()) {
                result.add(role.get(roleName));
            }
        }
        result.sort((r1, r2) -> r2.getPriority() - r1.getPriority());
        return result;
    }

    public boolean isDisabled() {
        return disabled;
    }
}

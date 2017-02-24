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
import java.util.List;
import java.util.HashMap;
import java.util.Map;

public class SlothCachedDomain {
    private String id;
    private String name;
    private Map<String, SlothCachedRole> role;
    private boolean disabled;

    public SlothCachedDomain(Domain domain) {
        id = domain.getId();
        name = domain.getName();
        role = new HashMap<>();
        for (Role r : domain.getRole()) {
            role.put(r.getId(), new SlothCachedRole(r));
        }
        disabled = domain.isDisabled();
    }

    private class SlothCachedRole {
        private String id;
        private String name;
        private Integer priority;
        private List<String> permissionId;
        private boolean disabled;

        public SlothCachedRole(Role role) {
            id = role.getId();
            name = role.getName();
            priority = role.getPriority();
            permissionId = role.getPermissionId();
            disabled = role.isDisabled();
        }
    }
}

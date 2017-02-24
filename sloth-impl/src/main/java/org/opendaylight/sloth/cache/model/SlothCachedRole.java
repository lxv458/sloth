/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.cache.model;

import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.domains.domain.Role;

import java.util.List;

public class SlothCachedRole {
    private final String id;
    private final String name;
    private final int priority;
    private final List<String> permissionId;
    private final boolean disabled;

    public SlothCachedRole(Role role) {
        id = role.getId();
        name = role.getName();
        priority = role.getPriority();
        permissionId = role.getPermissionId();
        disabled = role.isDisabled();
    }

    public int getPriority() {
        return priority;
    }

    public List<String> getPermissionId() {
        return permissionId;
    }

    public String getName() {
        return name;
    }
}

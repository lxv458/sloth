/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.cache.model;


import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.permissions.Permission;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.permissions.permission.ParamJson;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.permissions.permission.ParamQuery;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.HttpType;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.check.permission.input.Request;

import java.util.ArrayList;
import java.util.List;

public class SlothCachedPermission {
    private final String id;
    private final String name;
    private final List<String> resource;
    private final List<HttpType> action;
    private final List<SlothCachedParam> paramQuery;
    private final List<SlothCachedParam> paramJson;
    private final boolean disabled;

    public SlothCachedPermission(Permission permission) {
        id = permission.getId();
        name = permission.getName();
        resource = permission.getResource();
        action = permission.getAction();
        paramQuery = new ArrayList<>();
        for (ParamQuery q : permission.getParamQuery()) {
            paramQuery.add(new SlothCachedParam(q));
        }
        paramJson = new ArrayList<>();
        for (ParamJson j : permission.getParamJson()) {
            paramJson.add(new SlothCachedParam(j));
        }
        disabled = permission.isDisabled();
    }

    public SlothPermissionCheckResult isContradictory(Request request) {
        return new SlothPermissionCheckResult(true, "");
    }
}

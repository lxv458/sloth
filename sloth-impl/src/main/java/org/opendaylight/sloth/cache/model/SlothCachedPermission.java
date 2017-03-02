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

import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.regex.Pattern;

public class SlothCachedPermission {
    private final String id;
    private final String name;
    private final List<String> resourceList;
    private final Set<HttpType> actionList;
    private final List<ParamQuery> paramQueryList;
    private final List<ParamJson> paramJsonList;
    private final boolean disabled;

    public SlothCachedPermission(Permission permission) {
        id = permission.getId();
        name = permission.getName();
        resourceList = permission.getResource();
        actionList = new HashSet<>(permission.getAction());
        paramQueryList = permission.getParamQuery();
        paramJsonList = permission.getParamJson();
        disabled = permission.isDisabled();
    }

    public SlothPermissionCheckResult isContradictory(SlothRequest request) {
        for (String resource : resourceList) {
            if (actionList.contains(request.getMethod()) && Pattern.matches(resource, request.getRequestUrl())) {
                if (paramQueryList != null && paramQueryList.isEmpty()) {
                    for (ParamQuery paramQuery : paramQueryList) {
                        if (request.getQueryString().containsKey(paramQuery.getParam())) {
                            boolean flag = false;
                            for (String value : paramQuery.getValue()) {
                                if (Pattern.matches(value, request.getQueryString().get(paramQuery.getParam()))) {
                                    flag = true;
                                    break;
                                }
                            }
                            if (!flag) {
                                return new SlothPermissionCheckResult(false, "query string check failure");
                            }
                        }
                    }
                }
                if (paramJsonList != null && paramJsonList.isEmpty()) {
                    for (ParamJson paramJson : paramJsonList) {
                        boolean flag = false;
                        String v = request.getJsonPath().get(paramJson.getParam());
                        for (String value : paramJson.getValue()) {
                            if (Pattern.matches(value, v)) {
                                flag = true;
                                break;
                            }
                        }
                        if (!flag) {
                            return new SlothPermissionCheckResult(false, "json data check failure");
                        }
                    }
                }
            }
        }
        return new SlothPermissionCheckResult(true, null);
    }

    public boolean isDisabled() {
        return disabled;
    }
}

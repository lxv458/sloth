/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.cache.model;


import com.jayway.jsonpath.JsonPath;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.permissions.Permission;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.permissions.permission.ParamJson;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.permissions.permission.ParamQuery;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.HttpType;

import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.regex.Pattern;
import java.util.stream.Collectors;

public class SlothCachedPermission {
    private final List<Pattern> resourceList;
    private final Set<HttpType> actionList;
    private final List<SlothParamCheck> paramQueryList;
    private final List<SlothParamCheck> paramJsonList;
    private final boolean disabled;

    public SlothCachedPermission(Permission permission) {
        resourceList = permission.getResource().stream().map(Pattern::compile).collect(Collectors.toList());
        actionList = new HashSet<>(permission.getAction());
        paramQueryList = permission.getParamQuery().stream().map(SlothParamCheck::new).collect(Collectors.toList());
        paramJsonList = permission.getParamJson().stream().map(SlothParamCheck::new).collect(Collectors.toList());
        disabled = permission.isDisabled();
    }

    private class SlothParamCheck {
        private String param;
        private List<Pattern> value;
        private SlothParamCheck(ParamQuery paramQuery) {
            param = paramQuery.getParam();
            value = paramQuery.getValue().stream().map(Pattern::compile).collect(Collectors.toList());
        }
        private SlothParamCheck(ParamJson paramJson) {
            param = paramJson.getParam();
            value = paramJson.getValue().stream().map(Pattern::compile).collect(Collectors.toList());
        }
        private String getParam() {
            return param;
        }
        private List<Pattern> getValue() {
            return value;
        }
    }

    public SlothPermissionCheckResult isContradictory(SlothRequest request) {
        for (Pattern resource : resourceList) {
            if (actionList.contains(request.getMethod()) && resource.matcher(request.getRequestUrl()).matches()) {
                if (paramQueryList != null && paramQueryList.isEmpty() && !request.getQueryString().isEmpty()) {
                    for (SlothParamCheck paramQuery : paramQueryList) {
                        if (request.getQueryString().containsKey(paramQuery.getParam())) {
                            boolean flag = false;
                            for (Pattern value : paramQuery.getValue()) {
                                if (value.matcher(request.getQueryString().get(paramQuery.getParam())).matches()) {
                                    flag = true;
                                    break;
                                }
                            }
                            if (!flag) {
                                return new SlothPermissionCheckResult(false, "query string check failure: " + request.getQueryString());
                            }
                        }
                    }
                }
                if (paramJsonList != null && paramJsonList.isEmpty() && request.getDocument() != null) {
                    for (SlothParamCheck paramJson : paramJsonList) {
                        boolean flag = false;
                        String v = JsonPath.read(request.getDocument(), paramJson.getParam());
                        for (Pattern value : paramJson.getValue()) {
                            if (value.matcher(v).matches()) {
                                flag = true;
                                break;
                            }
                        }
                        if (!flag) {
                            return new SlothPermissionCheckResult(false, "json data check failure: " + paramJson.getParam());
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

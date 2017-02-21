/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.cache.model;


import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.ParamCheck;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.permissions.Permission;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.permissions.permission.ParamJson;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.permissions.permission.ParamQuery;

import java.util.ArrayList;
import java.util.List;

public class SlothCachedPermission {
    private String id;
    private List<String> resource;
    private List<String> action;
    private List<SlothCachedParam> paramQuery;
    private List<SlothCachedParam> paramJson;
    private boolean disabled;

    public SlothCachedPermission(Permission permission) {
        id = permission.getId();
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

    private class SlothCachedParam {
        public SlothCachedParam(ParamQuery paramQuery) {
            new SlothCachedParam(paramQuery.getParam(), paramQuery.getOperator(), paramQuery.getValue());
        }
        public SlothCachedParam(ParamJson paramJson) {
            new SlothCachedParam(paramJson.getParam(), paramJson.getOperator(), paramJson.getValue());
        }
        public SlothCachedParam(String param, ParamCheck.Operator operator, List<String> value) {
            this.param = param;
            this.operator = operator;
            this.value = new ArrayList<>(value);
        }
        private String param;
        private ParamCheck.Operator operator;
        private List<String> value;
    }
}

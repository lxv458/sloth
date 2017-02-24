/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.cache.model;

import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.OperatorType;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.permissions.permission.ParamJson;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.permissions.permission.ParamQuery;

import java.util.List;

public class SlothCachedParam {
    public SlothCachedParam(ParamQuery paramQuery) {
        this.param = paramQuery.getParam();
        this.operator = paramQuery.getOperator();
        this.value = paramQuery.getValue();
    }
    public SlothCachedParam(ParamJson paramJson) {
        this.param = paramJson.getParam();
        this.operator = paramJson.getOperator();
        this.value = paramJson.getValue();
    }
    private final String param;
    private final OperatorType operator;
    private final List<String> value;
}

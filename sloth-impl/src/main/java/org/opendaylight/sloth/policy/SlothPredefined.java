/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
package org.opendaylight.sloth.policy;


import java.util.HashMap;
import java.util.Map;
import java.util.Objects;

public enum SlothPredefined {
    SLOTH_SUBJECT_ROLE(0, "sloth.subject.role"), SLOTH_SUBJECT_USER_NAME(1, "sloth.subject.user_name"),
    SLOTH_ACTION_METHOD(2, "sloth.action.method"), SLOTH_ACTION_URL(3, "sloth.action.url"),
    SLOTH_ACTION_QUERY_STRING(4, "sloth.action.query_string"), SLOTH_ENVIRONMENT_DATE(5, "sloth.environment.date"),
    SLOTH_ENVIRONMENT_TIME(6, "sloth.environment.time"),
    SLOTH_ENVIRONMENT_DAY_OF_WEEK(7, "sloth.environment.day_of_week");
    private static final Map<Integer, SlothPredefined> VALUE_MAP;

    static {
        VALUE_MAP = new HashMap<>();
        for (SlothPredefined result : SlothPredefined.values()) {
            VALUE_MAP.put(result.getIntValue(), result);
        }
    }

    private int value;
    private String name;

    SlothPredefined(int value, String name) {
        this.value = value;
        this.name = name;
    }

    public static SlothPredefined forValue(int value) {
        return VALUE_MAP.get(value);
    }

    public static SlothPredefined parse(String name) {
        for (SlothPredefined v : VALUE_MAP.values()) {
            if (Objects.equals(v.getName(), name)) {
                return v;
            }
        }
        throw new IllegalArgumentException(name);
    }

    public String getName() {
        return name;
    }

    public int getIntValue() {
        return value;
    }
}

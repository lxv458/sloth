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

public enum ElementType {
    NULL(0, "NULL"), FLOAT(1, "FLOAT"), STRING(2, "STRING"), BOOLEAN(3, "BOOLEAN"),
    JSON_PATH(4, "JSON_PATH"), SLOTH_PREDEFINED(5, "SLOTH_PREDEFINED");
    private static final Map<Integer, ElementType> VALUE_MAP;

    static {
        VALUE_MAP = new HashMap<>();
        for (ElementType result : ElementType.values()) {
            VALUE_MAP.put(result.getIntValue(), result);
        }
    }

    private int value;
    private String name;

    ElementType(int value, String name) {
        this.value = value;
        this.name = name;
    }

    public static ElementType forValue(int value) {
        return VALUE_MAP.get(value);
    }

    public String getName() {
        return name;
    }

    public int getIntValue() {
        return value;
    }
}

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

public enum Result {
    ACCEPT(1, "ACCEPT"), REJECT(-1, "REJECT"), UNKNOWN(0, "UNKNOWN");
    private int value;
    private String name;
    private static final Map<Integer, Result> VALUE_MAP;

    static {
        VALUE_MAP = new HashMap<>();
        for (Result result : Result.values()) {
            VALUE_MAP.put(result.getIntValue(), result);
        }
    }

    private Result(int value, String name) {
        this.value = value;
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public int getIntValue() {
        return value;
    }

    public static Result forValue(int value) {
        return VALUE_MAP.get(value);
    }
}

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

public enum CheckResult {
    ACCEPT(1, "ACCEPT"), REJECT(-1, "REJECT"), UNKNOWN(0, "UNKNOWN");
    private static final Map<Integer, CheckResult> VALUE_MAP;

    static {
        VALUE_MAP = new HashMap<>();
        for (CheckResult checkResult : CheckResult.values()) {
            VALUE_MAP.put(checkResult.getIntValue(), checkResult);
        }
    }

    private int value;
    private String name;

    CheckResult(int value, String name) {
        this.value = value;
        this.name = name;
    }

    public static CheckResult forValue(int value) {
        return VALUE_MAP.get(value);
    }

    public String getName() {
        return name;
    }

    public int getIntValue() {
        return value;
    }
}

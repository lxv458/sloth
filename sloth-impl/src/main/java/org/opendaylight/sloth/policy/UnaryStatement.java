/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
package org.opendaylight.sloth.policy;


import org.opendaylight.sloth.cache.model.SlothRequest;

public class UnaryStatement implements Statement {
    private final CheckResult checkResult;

    public UnaryStatement(CheckResult checkResult) {
        this.checkResult = checkResult;
    }

    public CheckResult getCheckResult() {
        return checkResult;
    }

    @Override
    public CheckResult Check(SlothRequest input) {
        return checkResult;
    }

    @Override
    public String toString() {
        return toString(0);
    }

    @Override
    public String toString(int indent) {
        return (indent > 0 ? String.format("%" + indent + "s", "") : "") + checkResult.getName();
    }
}

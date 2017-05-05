/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
package org.opendaylight.sloth.policy;


import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.CheckPermissionInput;

public class UnaryStatement implements Statement {
    private final Result result;

    public UnaryStatement(Result result) {
        this.result = result;
    }

    public Result getResult() {
        return result;
    }

    @Override
    public Result Check(CheckPermissionInput input) {
        return result;
    }

    @Override
    public String toString() {
        return toString(0);
    }

    @Override
    public String toString(int indent) {
        return (indent > 0 ? String.format("%" + indent + "s", "") : "") + result.getName();
    }
}

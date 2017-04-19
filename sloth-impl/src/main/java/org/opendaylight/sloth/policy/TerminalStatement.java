/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
package org.opendaylight.sloth.policy;


public class TerminalStatement implements Statement {
    private final Result result;

    public TerminalStatement(Result result) {
        this.result = result;
    }

    public Result getResult() {
        return result;
    }

    @Override
    public Result Check() {
        return result;
    }
}

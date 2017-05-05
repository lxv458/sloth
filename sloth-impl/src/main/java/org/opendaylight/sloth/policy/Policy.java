/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
package org.opendaylight.sloth.policy;


import org.opendaylight.sloth.cache.model.SlothRequest;

public class Policy {
    private final String name;
    private final Statement statement;

    public Policy(String name, Statement statement) {
        this.name = name;
        this.statement = statement;
    }

    public Result Check(SlothRequest input) {
        return statement.Check(input);
    }

    @Override
    public String toString() {
        return name + "\n" + statement.toString();
    }
}

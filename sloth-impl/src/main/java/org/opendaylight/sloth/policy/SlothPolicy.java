/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
package org.opendaylight.sloth.policy;


import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.CheckPermissionInput;

public class SlothPolicy {
    private Statement statement;

    public Result Check(CheckPermissionInput input) {
        return statement.Check(input);
    }
}

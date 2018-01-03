/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.cache.model;

public class SlothPolicyCheckResult {
    private final Boolean success;
    private final Boolean check;
    private final String message;


    public SlothPolicyCheckResult(Boolean success, String message, Boolean check) {
        this.success = success;
        this.message = message;
        this.check = check;
    }

    public String getMessage() {
        return message;
    }

    public Boolean isSuccess() {
        return success;
    }

    public Boolean isCheck() { return check; }
}

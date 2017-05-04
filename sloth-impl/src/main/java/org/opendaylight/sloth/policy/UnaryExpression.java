/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
package org.opendaylight.sloth.policy;


import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.CheckPermissionInput;

public class UnaryExpression implements Expression {
    private final Object value;
    private final ElementType elementType;

    public UnaryExpression(Object value, ElementType elementType) {
        this.value = value;
        this.elementType = elementType;
    }

    @Override
    public ExprValue Evaluate(CheckPermissionInput input) {
        ExprValue exprValue = null;
        switch (elementType) {
            case JSON_PATH:
                break;
            case SLOTH_PREDEFINED:
                break;
            default:
                exprValue = new ExprValue(value, elementType);
                break;
        }
        return exprValue;
    }

    @Override
    public String toString() {
        return value.toString();
    }
}

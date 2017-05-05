/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
package org.opendaylight.sloth.policy;


import org.opendaylight.sloth.cache.model.SlothRequest;

public class UnaryExpression implements Expression {
    /*
    * The value here is defined as object.
    * It should be casted to actual value, according to ElementType.
    * Here is the mapping:
    * ElementType.NULL                  =>     null
    * ElementType.FLOAT                 =>     Float
    * ElementType.STRING                =>     String
    * ElementType.BOOLEAN               =>     Boolean
    * ElementType.JSON_PATH             =>     String
    * ElementType.SLOTH_PREDEFINED      =>     SlothPredefined
    *
    * SlothPredefined is for extensibility.
    * */
    private final Object value;
    private final ElementType elementType;

    public UnaryExpression(Object value, ElementType elementType) {
        this.value = value;
        this.elementType = elementType;
    }

    @Override
    public ExprValue Evaluate(SlothRequest input) {
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

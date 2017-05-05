/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
package org.opendaylight.sloth.policy;


import org.opendaylight.sloth.cache.model.SlothRequest;

import java.util.Objects;
import java.util.regex.Pattern;

public class BinaryExpression implements Expression {
    private final Expression leftExpression, rightExpression;
    private final Operator operator;

    public BinaryExpression(Expression leftExpression, Expression rightExpression, Operator operator) {
        this.leftExpression = leftExpression;
        this.rightExpression = rightExpression;
        this.operator = operator;
    }

    @Override
    public ExprValue Evaluate(SlothRequest input) {
        ExprValue leftExprVal = leftExpression.Evaluate(input), rightExprVal = rightExpression.Evaluate(input);
        ExprValue evalResult = null;
        if (operator == Operator.LT || operator == Operator.LE || operator == Operator.GT || operator == Operator.GE) {
            if (leftExprVal.getType() != ElementType.FLOAT || rightExprVal.getType() != ElementType.FLOAT) {
                throw new IllegalArgumentException(operator.getName() + ": left/right side type not integer or float");
            }
            Float left = (Float) leftExprVal.getValue(), right = (Float) rightExprVal.getValue();
            evalResult = new ExprValue(operator == Operator.LT ? left < right :
                    (operator == Operator.LE ? left <= right :
                            (operator == Operator.GT ? left > right : left >= right)), ElementType.BOOLEAN);
        } else if (operator == Operator.AND || operator == Operator.OR) {
            if (leftExprVal.getType() != ElementType.BOOLEAN || rightExprVal.getType() != ElementType.BOOLEAN) {
                throw new IllegalArgumentException(operator.getName() + ": left/right side not boolean");
            }
            Boolean left = (Boolean) leftExprVal.getValue(), right = (Boolean) rightExprVal.getValue();
            evalResult = new ExprValue(operator == Operator.AND ? (left && right) : (left || right), ElementType.BOOLEAN);
        } else if (operator == Operator.EQ || operator == Operator.NEQ) {
            if (leftExprVal.getType() == ElementType.FLOAT && rightExprVal.getType() == ElementType.FLOAT) {
                Float left = (Float) leftExprVal.getValue(), right = (Float) rightExprVal.getValue();
                evalResult = new ExprValue((operator == Operator.EQ) == Objects.equals(left, right), ElementType.BOOLEAN);
            } else if (leftExprVal.getType() == ElementType.STRING && rightExprVal.getType() == ElementType.STRING) {
                String left = (String) leftExprVal.getValue(), right = (String) rightExprVal.getValue();
                evalResult = new ExprValue((operator == Operator.EQ) == Objects.equals(left, right), ElementType.BOOLEAN);
            } else if (leftExprVal.getType() == ElementType.BOOLEAN && rightExprVal.getType() == ElementType.BOOLEAN) {
                Boolean left = (Boolean) leftExprVal.getValue(), right = (Boolean) rightExprVal.getValue();
                evalResult = new ExprValue((operator == Operator.EQ) == Objects.equals(left, right), ElementType.BOOLEAN);
            } else {
                throw new IllegalArgumentException(operator.getName() + ": left/right should be the same type of number, string or boolean");
            }
        } else if (operator == Operator.REG) {
            if (leftExprVal.getType() != ElementType.STRING) {
                throw new IllegalArgumentException(operator.getName() + ": left side not string");
            }
            if (rightExprVal.getType() != ElementType.STRING) {
                throw new IllegalArgumentException(operator.getName() + ": right side not regular expression");
            }
            evalResult = new ExprValue(Pattern.matches((String) leftExprVal.getValue(), (String) rightExprVal.getValue()) ||
                    Pattern.matches((String) rightExprVal.getValue(), (String) leftExprVal.getValue()), ElementType.BOOLEAN);
        }
        return evalResult;
    }

    @Override
    public String toString() {
        return String.format("(%s %s %s)", leftExpression.toString(), operator.getName(), rightExpression.toString());
    }
}

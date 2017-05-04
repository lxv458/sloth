/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
package org.opendaylight.sloth.policy;


import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.CheckPermissionInput;

public class BinaryStatement implements Statement {
    private final Expression expression;
    private final Statement thenStatement, elseStatement;

    public BinaryStatement(Expression expression, Statement thenStatement, Statement elseStatement) {
        this.expression = expression;
        this.thenStatement = thenStatement;
        this.elseStatement = elseStatement;
    }

    @Override
    public Result Check(CheckPermissionInput input) {
        ExprValue exprValue = expression.Evaluate(input);
        if (exprValue.getType() == ElementType.BOOLEAN) {
            return (Boolean)exprValue.getValue() ? thenStatement.Check(input) :
            (elseStatement != null ? elseStatement.Check(input) : Result.UNKNOWN);
        } else {
            throw new IllegalArgumentException("expression type not boolean");
        }
    }

    @Override
    public String toString() {
        return toString(0);
    }

    @Override
    public String toString(int indent) {
        String spaces = String.format("%1$#" + indent + "s", "");
        String exprStr = expression instanceof UnaryExpression ? "(" + expression.toString() + ")" : expression.toString();
        if (elseStatement != null) {
            return String.format("%sif %s {\n%s\n%s} else {\n%s\n%s}", spaces,
                    exprStr, thenStatement.toString(indent + 4), spaces,
                    elseStatement.toString(indent + 4), spaces);
        } else {
            return String.format("%sif %s {\n%s\n%s}", spaces, exprStr, thenStatement.toString(indent + 4), spaces);
        }
    }
}

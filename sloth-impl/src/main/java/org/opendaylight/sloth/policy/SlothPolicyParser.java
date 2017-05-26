/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
package org.opendaylight.sloth.policy;


import org.antlr.v4.runtime.ANTLRFileStream;
import org.antlr.v4.runtime.ANTLRInputStream;
import org.antlr.v4.runtime.CommonTokenStream;
import org.antlr.v4.runtime.misc.Interval;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.SlothPolicyHub;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.SlothPolicyHubBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.policies.PolicySet;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.policies.PolicySetBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.sloth.policy.hub.GlobalPolicySetBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.sloth.policy.hub.LocalPolicySet;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.sloth.policy.hub.LocalPolicySetBuilder;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;

public class SlothPolicyParser {
    public static SlothPolicyHub parseFile(String fileName) throws IOException {
        return new SlothPolicyFileParser(fileName).parse();
    }

    public static Statement parsePolicy(String policyText) throws IOException {
        return new SlothSinglePolicyParser(policyText).parse();
    }

    private static class SlothPolicyFileParser extends SlothPolicyRuleBaseVisitor<String> {
        private final SlothPolicyHubBuilder slothPolicyHubBuilder;

        public SlothPolicyFileParser(String fileName) throws IOException {
            slothPolicyHubBuilder = new SlothPolicyHubBuilder();
            ANTLRInputStream antlrInputStream = new ANTLRFileStream(fileName);
            SlothPolicyRuleLexer slothPolicyRuleLexer = new SlothPolicyRuleLexer(antlrInputStream);
            CommonTokenStream commonTokenStream = new CommonTokenStream(slothPolicyRuleLexer);
            SlothPolicyRuleParser slothPolicyRuleParser = new SlothPolicyRuleParser(commonTokenStream);
            SlothPolicyRuleParser.PolicySetContext policySetContext = slothPolicyRuleParser.policySet();
            visit(policySetContext);
        }

        private static List<PolicySet> getPolicySetList(List<SlothPolicyRuleParser.PolicyStatementContext> list) {
            List<PolicySet> policySetList = new ArrayList<>();
            PolicySetBuilder policySetBuilder = new PolicySetBuilder();
            for (SlothPolicyRuleParser.PolicyStatementContext psc : list) {
                policySetBuilder.setId(UUID.randomUUID().toString());
                policySetBuilder.setName(psc.Identifier().getText());
                policySetBuilder.setContent(psc.start.getInputStream().getText(
                        new Interval(psc.statement().start.getStartIndex(), psc.statement().stop.getStopIndex())));
                policySetList.add(policySetBuilder.build());
            }
            return policySetList;
        }

        public SlothPolicyHub parse() {
            return slothPolicyHubBuilder.build();
        }

        @Override
        public String visitPolicySet(SlothPolicyRuleParser.PolicySetContext ctx) {
            return visitChildren(ctx);
        }

        @Override
        public String visitGlobalPolicySet(SlothPolicyRuleParser.GlobalPolicySetContext ctx) {
            GlobalPolicySetBuilder globalPolicySetBuilder = new GlobalPolicySetBuilder();
            globalPolicySetBuilder.setPolicySet(getPolicySetList(ctx.policyStatement()));
            slothPolicyHubBuilder.setGlobalPolicySet(globalPolicySetBuilder.build());
            return null;
        }

        @Override
        public String visitLocalPolicySet(SlothPolicyRuleParser.LocalPolicySetContext ctx) {
            List<LocalPolicySet> localPolicySetList = new ArrayList<>();
            LocalPolicySetBuilder localPolicySetBuilder = new LocalPolicySetBuilder();
            for (SlothPolicyRuleParser.LocalPolicyStatementContext lpsc : ctx.localPolicyStatement()) {
                localPolicySetBuilder.setId(lpsc.Identifier(0).getText() + ":" + lpsc.Identifier(1).getText());
                localPolicySetBuilder.setPolicySet(getPolicySetList(lpsc.policyStatement()));
                localPolicySetList.add(localPolicySetBuilder.build());
            }
            slothPolicyHubBuilder.setLocalPolicySet(localPolicySetList);
            return null;
        }
    }

    private static class SlothSinglePolicyParser extends SlothPolicyRuleBaseVisitor<String> {
        private Statement statement;

        public SlothSinglePolicyParser(String policyText) {
            ANTLRInputStream antlrInputStream = new ANTLRInputStream(policyText);
            SlothPolicyRuleLexer slothPolicyRuleLexer = new SlothPolicyRuleLexer(antlrInputStream);
            CommonTokenStream commonTokenStream = new CommonTokenStream(slothPolicyRuleLexer);
            SlothPolicyRuleParser slothPolicyRuleParser = new SlothPolicyRuleParser(commonTokenStream);
            SlothPolicyRuleParser.StatementContext statementContext = slothPolicyRuleParser.statement();
            visit(statementContext);
        }

        private static Statement parseStatement(SlothPolicyRuleParser.StatementContext ctx) {
            if (ctx.getChildCount() == 1) {
                return new UnaryStatement(Result.valueOf(ctx.getText()));
            } else if (ctx.getChildCount() == 3) {
                return parseStatement(ctx.statement(0));
            } else {
                return new BinaryStatement(parseExpression(ctx.expression()),
                        parseStatement(ctx.statement(0)),
                        ctx.statement().size() > 1 ? parseStatement(ctx.statement(1)) : null);
            }
        }

        private static Expression parseExpression(SlothPolicyRuleParser.ExpressionContext ctx) {
            if (ctx.getChildCount() == 1) {
                if (ctx.primary().jsonpath() != null) {
                    return new UnaryExpression(ctx.getText(), ElementType.JSON_PATH);
                } else if (ctx.primary().slothPredefined() != null) {
                    return new UnaryExpression(SlothPredefined.parse(ctx.getText()), ElementType.SLOTH_PREDEFINED);
                } else if (ctx.primary().literal() != null) {
                    if (ctx.primary().literal().IntegerLiteral() != null || ctx.primary().literal().FloatLiteral() != null) {
                        return new UnaryExpression(Float.valueOf(ctx.getText()), ElementType.FLOAT);
                    } else if (ctx.primary().literal().StringLiteral() != null) {
                        return new UnaryExpression(ctx.getText(), ElementType.STRING);
                    } else if (ctx.primary().literal().BooleanLiteral() != null) {
                        return new UnaryExpression(Boolean.parseBoolean(ctx.getText()), ElementType.BOOLEAN);
                    } else if (ctx.primary().literal().NullLiteral() != null) {
                        return new UnaryExpression("null", ElementType.NULL);
                    } else {
                        throw new IllegalArgumentException("unknown primary literal expression: " + ctx.getText());
                    }
                } else {
                    throw new IllegalArgumentException("unknown primary expression: " + ctx.getText());
                }
            } else if (ctx.expression().size() == 1) {
                return parseExpression(ctx.expression(0));
            } else {
                return new BinaryExpression(parseExpression(ctx.expression(0)), parseExpression(ctx.expression(1)), Operator.parse(ctx.operator().getText()));
            }
        }

        @Override
        public String visitStatement(SlothPolicyRuleParser.StatementContext ctx) {
            statement = parseStatement(ctx);
            return null;
        }

        public Statement parse() throws IOException {
            return statement;
        }
    }
}

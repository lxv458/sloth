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

    public static Object parsePolicy(String policyText) throws IOException {
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

        private static List<PolicySet> getPolicySetList(List<SlothPolicyRuleParser.PolicyStatementContext> list) {
            List<PolicySet> policySetList = new ArrayList<>();
            PolicySetBuilder policySetBuilder = new PolicySetBuilder();
            for (SlothPolicyRuleParser.PolicyStatementContext psc : list) {
                policySetBuilder.setId(UUID.randomUUID().toString());
                policySetBuilder.setName(psc.Identifier().getText());
                policySetBuilder.setContent(psc.statement().getText());
                policySetList.add(policySetBuilder.build());
            }
            return policySetList;
        }
    }

    private static class SlothSinglePolicyParser extends SlothPolicyRuleBaseVisitor<String> {
        public SlothSinglePolicyParser(String policyText) {
            ANTLRInputStream antlrInputStream = new ANTLRInputStream(policyText);
            SlothPolicyRuleLexer slothPolicyRuleLexer = new SlothPolicyRuleLexer(antlrInputStream);
            CommonTokenStream commonTokenStream = new CommonTokenStream(slothPolicyRuleLexer);
            SlothPolicyRuleParser slothPolicyRuleParser = new SlothPolicyRuleParser(commonTokenStream);
            SlothPolicyRuleParser.PolicyStatementContext policyStatementContext = slothPolicyRuleParser.policyStatement();
            visit(policyStatementContext);
        }

        public Object parse() throws IOException {
            return null;
        }
    }
}

/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
package org.opendaylight.sloth.cache;


import com.google.common.cache.Cache;
import com.google.common.cache.CacheBuilder;
import org.opendaylight.controller.md.sal.binding.api.DataBroker;
import org.opendaylight.controller.md.sal.common.api.data.LogicalDatastoreType;
import org.opendaylight.sloth.cache.model.SlothPolicyCheckResult;
import org.opendaylight.sloth.cache.model.SlothRequest;
import org.opendaylight.sloth.policy.CheckResult;
import org.opendaylight.sloth.policy.Policy;
import org.opendaylight.sloth.policy.SlothPolicyParser;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.SlothPolicyHub;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.policies.PolicySet;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.sloth.policy.hub.GlobalPolicySet;
import org.opendaylight.yangtools.yang.binding.InstanceIdentifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.Map;
import java.util.Objects;


public class GlobalPolicyCache extends FilteredClusteredDTCListener<PolicySet> implements PolicyChecker {
    private static final Logger LOG = LoggerFactory.getLogger(GlobalPolicyCache.class);
    private static final InstanceIdentifier<PolicySet> GLOBAL_POLICY_SET_ID = InstanceIdentifier
            .create(SlothPolicyHub.class).child(GlobalPolicySet.class).child(PolicySet.class);
    private static final long MAX_GLOBAL_POLICY_CACHE = 100000;

    private final Cache<String, Policy> globalPolicyCache;

    public GlobalPolicyCache(DataBroker dataBroker) {
        super(dataBroker);
        registerListener(LogicalDatastoreType.CONFIGURATION, GLOBAL_POLICY_SET_ID);
        globalPolicyCache = CacheBuilder.newBuilder().maximumSize(MAX_GLOBAL_POLICY_CACHE).build();
        LOG.info("global policy cache initialized");
    }
    @Override
    protected void created(PolicySet after) {
        if (after != null) {
            LOG.info("create global policy: " + after.getName());
            try {
                globalPolicyCache.put(after.getId(),
                        new Policy(after.getName(), SlothPolicyParser.parsePolicy(after.getContent())));
            } catch (IOException e) {
                LOG.error("failed to create policy, parse error: " + after.getContent());
            }
        }
    }

    @Override
    protected void updated(PolicySet before, PolicySet after) {
        if (Objects.equals(before.getId(), after.getId())) {
            LOG.info("update global policy cache");
            if (globalPolicyCache.getIfPresent(before.getId()) != null) {
                try {
                    globalPolicyCache.put(after.getId(),
                            new Policy(after.getName(), SlothPolicyParser.parsePolicy(after.getContent())));
                } catch (IOException e) {
                    LOG.error("failed to update policy, parse error: " + after.getContent());
                }
            } else {
                LOG.error("failed to update global policy, policy not exist.");
            }
        } else {
            LOG.error("failed to update global policy, before: " + before.getName() + ", after: " + after.getName());
        }
    }

    @Override
    protected void deleted(PolicySet before) {
        if (before != null) {
            LOG.info("delete global policy: " + before.getName());
            globalPolicyCache.invalidate(before.getId());
        }
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (Map.Entry<String, Policy> entry : globalPolicyCache.asMap().entrySet()) {
            sb.append(entry.getValue().toString()).append('\n');
        }
        return sb.toString();
    }

    @Override
    public SlothPolicyCheckResult policyCheck(SlothRequest input) {
        for (Map.Entry<String, Policy> entry : globalPolicyCache.asMap().entrySet()) {
            try {
                CheckResult r = entry.getValue().Check(input);
                if (r == CheckResult.ACCEPT) {
                    return new SlothPolicyCheckResult(true, "request is permitted by policy: " + entry.getValue().getName());
                } else if (r == CheckResult.REJECT) {
                    return new SlothPolicyCheckResult(false, "request is rejected by policy: " + entry.getValue().getName());
                }
            } catch (Exception e) {
                LOG.info("global policy check exception of policy: " + entry.getValue().getName());
                LOG.info(e.getMessage());
            }
        }
        return new SlothPolicyCheckResult(null, "request matches none of the policies");
    }
}

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
import org.opendaylight.sloth.policy.SlothPolicyParser;
import org.opendaylight.sloth.policy.Statement;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.SlothPolicyHub;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.policies.PolicySet;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.sloth.policy.hub.LocalPolicySet;
import org.opendaylight.yangtools.yang.binding.InstanceIdentifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.Objects;

public class LocalPolicyCache extends FilteredClusteredDTCListener<LocalPolicySet> {
    private static final Logger LOG = LoggerFactory.getLogger(LocalPolicyCache.class);
    private static final InstanceIdentifier<LocalPolicySet> LOCAL_POLICY_SET_ID = InstanceIdentifier
            .create(SlothPolicyHub.class).child(LocalPolicySet.class);
    private static final long MAX_LOCAL_POLICY_CACHE = 100000, MAX_LOCAL_POLICY_INDIVIDUAL_CACHE = 100000;

    private final Cache<String, Cache<String, Statement>> localPolicyCache;

    public LocalPolicyCache(DataBroker dataBroker) {
        super(dataBroker);
        registerListener(LogicalDatastoreType.CONFIGURATION, LOCAL_POLICY_SET_ID);
        localPolicyCache = CacheBuilder.newBuilder().maximumSize(MAX_LOCAL_POLICY_CACHE).build();
        LOG.info("local policy cache initialized");
    }

    @Override
    protected void created(LocalPolicySet after) {
        if (after != null) {
            LOG.info("create local policy: " + after.getId());
            Cache<String, Statement> cache = CacheBuilder.newBuilder().maximumSize(MAX_LOCAL_POLICY_INDIVIDUAL_CACHE).build();
            localPolicyCache.put(after.getId(), cache);
            for (PolicySet policy : after.getPolicySet()) {
                try {
                    cache.put(policy.getId(), SlothPolicyParser.parsePolicy(policy.getContent()));
                } catch (IOException e) {
                    LOG.error("local policy creation error, failed to parse policy: " + policy.getContent());
                }
            }
        }
    }

    @Override
    protected void updated(LocalPolicySet before, LocalPolicySet after) {
        /*
        * The update strategy can be optimized here.
        * Currently, we will delete the whole cache under certain local id.
        * Definitely, we can just update the exact policy of the certain cache.
        * But, luckily, update operation for a policy cache is not frequent.
        * */
        if (Objects.equals(before.getId(), after.getId())) {
            if (localPolicyCache.getIfPresent(before.getId()) != null) {
                localPolicyCache.invalidate(before.getId());
                Cache<String, Statement> cache = CacheBuilder.newBuilder().maximumSize(MAX_LOCAL_POLICY_INDIVIDUAL_CACHE).build();
                localPolicyCache.put(after.getId(), cache);
                for (PolicySet policy : after.getPolicySet()) {
                    try {
                        cache.put(policy.getId(), SlothPolicyParser.parsePolicy(policy.getContent()));
                    } catch (IOException e) {
                        LOG.error("local policy creation error, failed to parse policy: " + policy.getContent());
                    }
                }
            } else {
                LOG.error("failed to update local policy, policy not exist: " + before.getId());
            }
        } else {
            LOG.error("failed to update local policy, before: " + before.getId() + ", after: " + after.getId());
        }
    }

    @Override
    protected void deleted(LocalPolicySet before) {
        if (before != null) {
            LOG.info("delete local policy: " + before.getId());
            localPolicyCache.invalidate(before.getId());
        }
    }
}

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
import org.opendaylight.sloth.cache.model.SlothCachedDomain;
import org.opendaylight.sloth.cache.model.SlothCachedRole;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.Domains;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.domains.Domain;
import org.opendaylight.yangtools.yang.binding.InstanceIdentifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;

public class SlothDomainCache extends FilteredClusteredDTCListener<Domain>{
    private static final Logger LOG = LoggerFactory.getLogger(SlothDomainCache.class);
    private static final InstanceIdentifier<Domain> SLOTH_DOMAIN_ID = InstanceIdentifier
            .create(Domains.class).child(Domain.class);
    private static final long MAX_DOMAIN_CACHE = 1000000;

    private final Cache<String, SlothCachedDomain> domainCache;

    public SlothDomainCache(DataBroker dataBroker) {
        super(dataBroker);
        registerListener(LogicalDatastoreType.CONFIGURATION, SLOTH_DOMAIN_ID);
        domainCache = CacheBuilder.newBuilder().maximumSize(MAX_DOMAIN_CACHE).build();
        LOG.info("initialize SlothDomainCache");
    }

    @Override
    protected void created(Domain after) {
        LOG.info("domain created: " + after.getName());
        domainCache.put(after.getName(), new SlothCachedDomain(after));
    }

    @Override
    protected void updated(Domain before, Domain after) {
        LOG.info("domain updated: " + after.getName());
        if (domainCache.getIfPresent(after.getName()) != null) {
            domainCache.put(after.getName(), new SlothCachedDomain(after));
        } else {
            LOG.error("domain cache update error: before name = " + before.getName() + ", after name = " + after.getName());
        }
    }

    @Override
    protected void deleted(Domain before) {
        LOG.info("domain deleted: " + before.getName());
        domainCache.invalidate(before.getName());
    }

    public List<SlothCachedRole> getRelatedSlothCachedRole(String domainName, List<String> roleNames) {
        List<SlothCachedRole> result = null;
        SlothCachedDomain domain = domainCache.getIfPresent(domainName);
        if (domain != null) {
            result = domain.getRelatedSlothCachedRole(roleNames);
        } else {
            LOG.error("domain cache can not find domain: " + domainName);
        }
        return result;
    }
}

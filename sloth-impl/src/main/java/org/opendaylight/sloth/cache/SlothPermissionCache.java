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
import org.opendaylight.sloth.cache.model.SlothCachedPermission;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.Permissions;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.permissions.Permission;
import org.opendaylight.yangtools.yang.binding.InstanceIdentifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class SlothPermissionCache extends FilteredClusteredDTCListener<Permission> {
    private static final Logger LOG = LoggerFactory.getLogger(SlothPermissionCache.class);
    private static final InstanceIdentifier<Permission> SLOTH_PERMISSION_ID = InstanceIdentifier
            .create(Permissions.class).child(Permission.class);
    private static final long MAX_PERMISSION_CACHE = 1000000;

    private final Cache<String, SlothCachedPermission> permissionCache;

    public SlothPermissionCache(DataBroker dataBroker) {
        super(dataBroker);
        registerListener(LogicalDatastoreType.CONFIGURATION, SLOTH_PERMISSION_ID);
        permissionCache = CacheBuilder.newBuilder().maximumSize(MAX_PERMISSION_CACHE).build();
        LOG.info("initialize SlothPermissionCache");
    }

    @Override
    protected void created(Permission after) {
        LOG.info("permission created: " + after.getId());
        permissionCache.put(after.getId(), new SlothCachedPermission(after));
    }

    @Override
    protected void updated(Permission before, Permission after) {
        LOG.info("permission updated: " + after.getId());
        if (permissionCache.getIfPresent(after.getId()) != null) {
            permissionCache.put(after.getId(), new SlothCachedPermission(after));
        } else {
            LOG.error("permission cache update error: before id = " + before.getId() + ", after id = " + after.getId());
        }
    }

    @Override
    protected void deleted(Permission before) {
        LOG.info("permission deleted: " + before.getId());
        permissionCache.invalidate(before.getId());
    }

    public SlothCachedPermission getSlothCachedPermission(String permissionId) {
        return permissionCache.getIfPresent(permissionId);
    }
}

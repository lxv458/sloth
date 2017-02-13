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
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.SlothPermissions;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.sloth.permissions.SlothPermission;
import org.opendaylight.yangtools.yang.binding.InstanceIdentifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class SlothPermissionCache extends FilteredClusteredDTCListener<SlothPermission> {
    private static final Logger LOG = LoggerFactory.getLogger(SlothPermissionCache.class);
    private static final InstanceIdentifier<SlothPermission> SLOTH_PERMISSION_ID = InstanceIdentifier
            .create(SlothPermissions.class).child(SlothPermission.class);
    private static final int MAX_PERMISSION_CACHE = 1000000;

    private final DataBroker dataBroker;
    private final Cache<String, SlothCachedPermission> permissionCache;

    public SlothPermissionCache(DataBroker dataBroker) {
        super(dataBroker);
        this.dataBroker = dataBroker;
        registerListener(LogicalDatastoreType.CONFIGURATION, SLOTH_PERMISSION_ID);
        permissionCache = CacheBuilder.newBuilder().maximumSize(MAX_PERMISSION_CACHE).build();
        LOG.info("initialize SlothPermissionCache");
    }

    @Override
    protected void created(SlothPermission after) {
        permissionCache.put(after.getUuid(), new SlothCachedPermission(after));
    }

    @Override
    protected void updated(SlothPermission before, SlothPermission after) {
        permissionCache.put(after.getUuid(), new SlothCachedPermission(after));
    }

    @Override
    protected void deleted(SlothPermission before) {
        permissionCache.invalidate(before.getUuid());
    }
}

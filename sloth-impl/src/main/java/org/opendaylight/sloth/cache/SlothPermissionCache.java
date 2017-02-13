/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.cache;


import org.opendaylight.controller.md.sal.binding.api.DataBroker;
import org.opendaylight.controller.md.sal.common.api.data.LogicalDatastoreType;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.SlothPermissions;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.sloth.permissions.SlothPermission;
import org.opendaylight.yangtools.yang.binding.InstanceIdentifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class SlothPermissionCache extends FilteredClusteredDTCListener<SlothPermission> {
    private static final Logger LOG = LoggerFactory.getLogger(SlothPermissionCache.class);
    private static final InstanceIdentifier<SlothPermission> SLOTH_PERMISSION_ID = InstanceIdentifier
            .create(SlothPermissions.class).child(SlothPermission.class);

    public SlothPermissionCache(DataBroker dataBroker) {
        super(dataBroker);
        registerListener(LogicalDatastoreType.CONFIGURATION, SLOTH_PERMISSION_ID);
    }

    @Override
    protected void created(InstanceIdentifier<SlothPermission> id, SlothPermission after) {

    }

    @Override
    protected void updated(InstanceIdentifier<SlothPermission> id, SlothPermission before, SlothPermission after) {

    }

    @Override
    protected void deleted(InstanceIdentifier<SlothPermission> id, SlothPermission before) {

    }
}

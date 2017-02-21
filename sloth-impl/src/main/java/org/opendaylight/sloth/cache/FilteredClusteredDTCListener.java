/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.cache;


import org.opendaylight.controller.md.sal.binding.api.ClusteredDataTreeChangeListener;
import org.opendaylight.controller.md.sal.binding.api.DataBroker;
import org.opendaylight.controller.md.sal.binding.api.DataObjectModification;
import org.opendaylight.controller.md.sal.binding.api.DataTreeIdentifier;
import org.opendaylight.controller.md.sal.binding.api.DataTreeModification;
import org.opendaylight.controller.md.sal.common.api.data.LogicalDatastoreType;
import org.opendaylight.yangtools.concepts.ListenerRegistration;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.binding.InstanceIdentifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.annotation.Nonnull;
import java.util.Collection;

public abstract class FilteredClusteredDTCListener<T extends DataObject> implements ClusteredDataTreeChangeListener<T>, AutoCloseable {
    private static final Logger LOG = LoggerFactory.getLogger(FilteredClusteredDTCListener.class);

    private final DataBroker dataBroker;
    private ListenerRegistration listenerRegistration;


    public FilteredClusteredDTCListener(final DataBroker dataBroker) {
        this.dataBroker = dataBroker;
    }

    protected abstract void created(T after);

    protected abstract void updated(T before, T after);

    protected abstract void deleted(T before);

    protected void registerListener(LogicalDatastoreType storeType, InstanceIdentifier<T> id) {
        listenerRegistration = dataBroker.registerDataTreeChangeListener(new DataTreeIdentifier<>(storeType, id), this);
        LOG.info("FilteredClusteredDTCListener registered success");
    }

    @Override
    public void onDataTreeChanged(@Nonnull Collection<DataTreeModification<T>> changes) {
        for (DataTreeModification<T> change : changes) {
            if (change.getRootNode().getModificationType() == DataObjectModification.ModificationType.WRITE ||
                    change.getRootNode().getModificationType() == DataObjectModification.ModificationType.SUBTREE_MODIFIED) {
                if (change.getRootNode().getDataBefore() == null) {
                    created(change.getRootNode().getDataAfter());
                } else {
                    updated(change.getRootNode().getDataBefore(), change.getRootNode().getDataAfter());
                }
            } else {
                deleted(change.getRootNode().getDataAfter());
            }
        }
    }

    @Override
    public void close() throws Exception {
        if (listenerRegistration != null) {
            listenerRegistration.close();
        }
    }
}

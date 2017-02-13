/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.service;

import org.opendaylight.controller.md.sal.binding.api.DataBroker;
import org.opendaylight.controller.sal.binding.api.BindingAwareBroker;
import org.opendaylight.controller.sal.binding.api.RpcProviderRegistry;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.sloth.rev150105.SlothPermissionService;
import org.osgi.framework.BundleContext;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class SlothServiceProvider {

    private static final Logger LOG = LoggerFactory.getLogger(SlothServiceProvider.class);

    private final DataBroker dataBroker;
    private final RpcProviderRegistry rpcProviderRegistry;
    private final BundleContext bundleContext;

    private SlothServiceFactory slothServiceFactory;

    private BindingAwareBroker.RpcRegistration<SlothPermissionService> rpcRegistration;

    public SlothServiceProvider(final DataBroker dataBroker, final RpcProviderRegistry rpcProviderRegistry,
                                final BundleContext bundleContext) {
        this.dataBroker = dataBroker;
        this.rpcProviderRegistry = rpcProviderRegistry;
        this.bundleContext = bundleContext;
    }

    /**
     * Method called when the blueprint container is created.
     */
    public void init() {
        slothServiceFactory = new SlothServiceFactoryImpl(dataBroker, rpcProviderRegistry, bundleContext, 10);
        LOG.info("SlothServiceProvider Session Initiated");
    }

    /**
     * Method called when the blueprint container is destroyed.
     */
    public void close() {
        try {
            slothServiceFactory.close();
        } catch (Exception e) {
            e.printStackTrace();
            LOG.info("failed to close SlothServiceFactory");
        }
        LOG.info("SlothServiceFactory Closed");
    }
}
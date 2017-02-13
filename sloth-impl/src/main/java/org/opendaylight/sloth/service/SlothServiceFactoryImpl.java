/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.service;


import com.google.common.base.Preconditions;
import org.opendaylight.controller.md.sal.binding.api.DataBroker;
import org.opendaylight.controller.sal.binding.api.BindingAwareBroker;
import org.opendaylight.controller.sal.binding.api.RpcProviderRegistry;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.sloth.rev150105.SlothPermissionService;
import org.osgi.framework.BundleContext;
import org.osgi.framework.ServiceRegistration;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class SlothServiceFactoryImpl implements SlothServiceFactory {
    private static final Logger LOG = LoggerFactory.getLogger(SlothServiceFactoryImpl.class);

    private final SlothPermissionService slothPermissionService;
    private final BindingAwareBroker.RpcRegistration<SlothPermissionService> slothPermissionServiceRpcRegistration;
    private ServiceRegistration serviceRegistration;

    public SlothServiceFactoryImpl(final DataBroker dataBroker, final RpcProviderRegistry rpcProviderRegistry,
                                   final BundleContext bundleContext, final int numOfRoutees) {
        slothPermissionService = new SlothPermissionEngine(dataBroker, bundleContext, numOfRoutees);
        slothPermissionServiceRpcRegistration = rpcProviderRegistry.addRpcImplementation(SlothPermissionService.class, slothPermissionService);
        registerService(bundleContext);
        LOG.info("SlothServiceFactoryImpl created");
    }

    private void registerService(BundleContext bundleContext) {
        Preconditions.checkNotNull(bundleContext, "can not register with null bundle context");
        if (serviceRegistration == null) {
            serviceRegistration = bundleContext.registerService(SlothServiceFactory.class.getName(), this, null);
            LOG.info("SlothServiceFactory successfully registered");
        } else {
            LOG.warn("SlothServiceFactory has already been registered");
        }
    }

    @Override
    public SlothPermissionService getSlothPermissionService() {
        return slothPermissionService;
    }

    @Override
    public void close() throws Exception {
        slothPermissionServiceRpcRegistration.close();
        serviceRegistration.unregister();
    }
}

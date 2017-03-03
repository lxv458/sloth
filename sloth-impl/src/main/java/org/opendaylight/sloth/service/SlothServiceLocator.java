/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.service;


import org.opendaylight.sloth.cache.SlothReadCache;
import org.opendaylight.sloth.exception.ServiceUnavailableException;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.SlothPermissionService;
import org.osgi.framework.BundleContext;
import org.osgi.framework.FrameworkUtil;
import org.osgi.framework.InvalidSyntaxException;
import org.osgi.framework.ServiceReference;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public final class SlothServiceLocator {
    private static final Logger LOG = LoggerFactory.getLogger(SlothServiceLocator.class);
    private static final SlothServiceLocator slothServiceLocator = new SlothServiceLocator();
    private SlothServiceFactory slothServiceFactory;

    public static SlothServiceLocator getInstance() {
        return slothServiceLocator;
    }

    public SlothPermissionService getPermissionService() throws ServiceUnavailableException {
        return getSlothServiceFactory().getSlothPermissionService();
    }

    public SlothReadCache getSlothReadCache() throws ServiceUnavailableException {
        return getSlothServiceFactory().getSlothReadCache();
    }

    private Object getServiceInstance(Class<?> clazz, Object bundle) {
        BundleContext bundleContext = FrameworkUtil.getBundle(bundle.getClass()).getBundleContext();
        try {
            ServiceReference<?>[] serviceReferences = bundleContext.getServiceReferences(clazz.getName(), null);
            if (serviceReferences != null) {
                return bundleContext.getService(serviceReferences[0]);
            } else {
                LOG.error("failed to get ServiceReferences");
            }
        } catch (InvalidSyntaxException e) {
            LOG.error("can not get bundle service instance in OSGi framework: " + e.getMessage());
        }
        return null;
    }

    private SlothServiceFactory getSlothServiceFactory() throws ServiceUnavailableException {
        if (slothServiceFactory == null) {
            slothServiceFactory = (SlothServiceFactory) getServiceInstance(SlothServiceFactory.class, this);
            if (slothServiceFactory == null) {
                throw new ServiceUnavailableException("failed to get SlothServiceFactory service in OSGi framework");
            }
        }
        return slothServiceFactory;
    }
}

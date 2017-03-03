/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.akka;


import akka.actor.ActorSystem;
import akka.osgi.BundleDelegatingClassLoader;
import com.google.common.base.Preconditions;
import org.osgi.framework.BundleContext;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import scala.concurrent.Await;
import scala.concurrent.duration.Duration;

import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

public class SlothActorSystem {
    private static final Logger LOG = LoggerFactory.getLogger(SlothActorSystem.class);
    private static ActorSystem actorSystem = null;

    public static synchronized ActorSystem createActorSystem(final BundleContext bundleContext) {
        if (actorSystem == null) {
            Preconditions.checkNotNull(bundleContext, "can not create actor system with empty bundle context");
            BundleDelegatingClassLoader classLoader = new BundleDelegatingClassLoader(bundleContext.getBundle(),
                    Thread.currentThread().getContextClassLoader());
            actorSystem = ActorSystem.create("SlothActorSystem", null, classLoader);
            LOG.info("successfully create actor system with osgi classloader");
        }
        return actorSystem;
    }

    public static synchronized void destroyActorSystem() {
        if (actorSystem != null) {
            try {
                actorSystem.terminate();
                Await.ready(actorSystem.whenTerminated(), Duration.create(10, TimeUnit.SECONDS));
            } catch (TimeoutException | InterruptedException e) {
                LOG.warn("fail to terminate actor system in 10 seconds: " + e.getMessage());
            }
            actorSystem = null;
            LOG.info("Sloth Actor System terminated");
        }
    }
}

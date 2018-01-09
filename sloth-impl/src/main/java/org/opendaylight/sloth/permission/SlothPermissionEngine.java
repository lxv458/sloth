/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
package org.opendaylight.sloth.permission;

import akka.actor.ActorRef;
import akka.actor.ActorSystem;
import akka.pattern.Patterns;
import org.opendaylight.controller.md.sal.binding.api.DataBroker;
import org.opendaylight.sloth.akka.SlothActorSystem;
import org.opendaylight.sloth.akka.SlothPermissionRouter;
import org.opendaylight.sloth.cache.model.SlothPolicyCheckResult;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.CheckPermissionInput;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.CheckPermissionOutput;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.CheckPermissionOutputBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.SlothPermissionService;
import org.opendaylight.yangtools.yang.common.RpcResult;
import org.opendaylight.yangtools.yang.common.RpcResultBuilder;
import org.osgi.framework.BundleContext;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import scala.concurrent.Await;
import scala.concurrent.duration.Duration;

import java.util.concurrent.Future;
import java.util.concurrent.TimeUnit;


public class SlothPermissionEngine implements SlothPermissionService, AutoCloseable {
    private static final Logger LOG = LoggerFactory.getLogger(SlothPermissionEngine.class);

    private final DataBroker dataBroker;
    private ActorSystem actorSystem;
    private final ActorRef permissionRouter;

    // used by service.SlothServiceFactoryImpl
    // numOfRoutees is set to 10 by SlothServiceProvider
    public SlothPermissionEngine(final DataBroker dataBroker, final BundleContext bundleContext, final int numOfRoutees) {
        this.dataBroker = dataBroker;
        actorSystem = SlothActorSystem.createActorSystem(bundleContext);
        permissionRouter = actorSystem.actorOf(SlothPermissionRouter.props(numOfRoutees));
    }

    // I just feel the permission check is not processed here
    // Or it is just processed by some third-part library. akka?
    @Override
    public Future<RpcResult<CheckPermissionOutput>> checkPermission(CheckPermissionInput input) {
        LOG.info("Come into PermissionEngine.checkPermission, next execute actor");
        scala.concurrent.Future<Object> result = Patterns.ask(permissionRouter, input, 5000);
        CheckPermissionOutputBuilder checkPermissionOutputBuilder = new CheckPermissionOutputBuilder();
        RpcResultBuilder<CheckPermissionOutput> resultBuilder;
        try {
            SlothPolicyCheckResult slothPolicyCheckResult = (SlothPolicyCheckResult) Await.result(result, Duration.create(5, TimeUnit.SECONDS));
            if (slothPolicyCheckResult.isSuccess()) {
                checkPermissionOutputBuilder.setStatusCode(200).setResponse(slothPolicyCheckResult.getMessage());
                LOG.info("accept status_code is 200");
            } else {
                checkPermissionOutputBuilder.setStatusCode(401).setResponse(slothPolicyCheckResult.getMessage());
                LOG.info("reject status_code is 401");
            }
            resultBuilder = RpcResultBuilder.success(checkPermissionOutputBuilder.build());
            LOG.info("SlothPermissionEngine success process permission check");
        } catch (Exception e) {
            resultBuilder = RpcResultBuilder.failed();
            LOG.warn("SlothPermissionEngine permission check failure: " + e.getMessage());
        }
        return resultBuilder.buildFuture();
    }

    @Override
    public void close() throws Exception {
        SlothActorSystem.destroyActorSystem();
        actorSystem = null;
    }
}

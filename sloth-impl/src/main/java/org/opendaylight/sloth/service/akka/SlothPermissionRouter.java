/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.service.akka;

import akka.actor.ActorRef;
import akka.actor.Props;
import akka.actor.UntypedActor;
import akka.japi.Creator;
import akka.routing.ActorRefRoutee;
import akka.routing.RoundRobinRoutingLogic;
import akka.routing.Routee;
import akka.routing.Router;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.sloth.rev150105.CheckPermissionInput;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;

public class SlothPermissionRouter extends UntypedActor {
    private static final Logger LOG = LoggerFactory.getLogger(SlothPermissionRouter.class);
    private final Router router;

    public SlothPermissionRouter(int numOfRoutees) {
        List<Routee> routees = new ArrayList<>(numOfRoutees);
        for (int i = 0; i < numOfRoutees; i++) {
            ActorRef actorRef= getContext().actorOf(SlothPermissionActor.props());
            getContext().watch(actorRef);
            routees.add(new ActorRefRoutee(actorRef));
        }
        router = new Router(new RoundRobinRoutingLogic(), routees);
    }

    @Override
    public void onReceive(Object o) throws Exception {
        if (o instanceof CheckPermissionInput) {
            LOG.info("SlothPermissionRouter receives CheckPermissionInput, routes to actor");
            router.route(o, getSender());
        } else {
            LOG.warn("SlothPermissionRouter receives unknow type of message: " + o);
        }
    }

    public static Props props(int numOfRoutees) {
        return Props.create(new SlothPermissionRouterCreator(numOfRoutees));
    }

    private static class SlothPermissionRouterCreator implements Creator<SlothPermissionRouter> {

        private final int numOfRoutees;

        public SlothPermissionRouterCreator(int numOfRoutees) {
            this.numOfRoutees = numOfRoutees;
        }

        @Override
        public SlothPermissionRouter create() throws Exception {
            return new SlothPermissionRouter(numOfRoutees);
        }
    }
}

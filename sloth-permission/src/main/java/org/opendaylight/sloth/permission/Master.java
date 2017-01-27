/*
 * Copyright (c) 2017 Northwestern University LIST Group. and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */


package org.opendaylight.sloth.permission;

import akka.actor.ActorRef;
import akka.actor.Props;
import akka.actor.UntypedActor;
import akka.routing.RoundRobinPool;

/**
 * All right reserved.
 * Northwestern University LIST Lab 2017.
 * Created by libin on 17-1-27.
 */
public class Master extends UntypedActor {
    private final ActorRef workerRouter;

    public Master(int numOfWorkers) {
        workerRouter = this.getContext().actorOf(Props.create(Worker.class).withRouter(new RoundRobinPool(numOfWorkers)),
                "workerRouter");
    }

    @Override
    public void onReceive(Object o) throws Exception {
        workerRouter.tell(o, getSelf());
    }
}

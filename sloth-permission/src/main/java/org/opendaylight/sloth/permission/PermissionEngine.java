/*
 * Copyright (c) 2017 Northwestern University LIST Group. and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.permission;

import akka.actor.ActorRef;
import akka.actor.ActorSystem;
import akka.actor.Props;
import akka.japi.Creator;

import javax.servlet.ServletRequest;

/**
 * All right reserved.
 * Northwestern University LIST Lab 2017.
 * Created by libin on 17-1-26.
 */
public class PermissionEngine {
    private static boolean initialized;
    private static ActorRef master;

    public static void init(int numOfWorkers) {
        initialized = true;
        ActorSystem system = ActorSystem.create("SlothSecuritySystem");
        master = system.actorOf(Props.create(new Creator<Master>() {
            @Override
            public Master create() throws Exception {
                return new Master(numOfWorkers);
            }
        }), "Master");
    }

    public static boolean checkPermission(ServletRequest request) {
        master.tell(request, ActorRef.noSender());
        return false;
    }

    public static void destroy() {
        if (initialized) {

        }
    }
}

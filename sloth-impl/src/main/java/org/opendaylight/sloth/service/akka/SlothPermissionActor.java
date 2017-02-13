/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.service.akka;

import akka.actor.Props;
import akka.actor.UntypedActor;
import akka.japi.Creator;
import org.opendaylight.yang.gen.v1.urn.opendaylight.params.xml.ns.yang.sloth.rev150105.CheckPermissionInput;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class SlothPermissionActor extends UntypedActor {
    private static final Logger LOG = LoggerFactory.getLogger(SlothPermissionActor.class);

    @Override
    public void onReceive(Object o) throws Exception {
        if (o instanceof CheckPermissionInput) {
            LOG.info("SlothPermissionActor receives CheckpermissionInput");
            CheckPermissionInput input = (CheckPermissionInput) o;
            getSender().tell("Got your message", getSelf());
        } else {
            LOG.warn("SlothPermissionActor receives unknown type message: " + o);
        }
    }

    public static Props props() {
        return Props.create(new SlothPermissionActorCreator());
    }

    private static class SlothPermissionActorCreator implements Creator<SlothPermissionActor> {

        @Override
        public SlothPermissionActor create() throws Exception {
            return new SlothPermissionActor();
        }
    }
}

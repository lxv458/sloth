/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.akka;

import akka.actor.Props;
import akka.actor.UntypedActor;
import akka.japi.Creator;
import org.opendaylight.sloth.cache.SlothReadCache;
import org.opendaylight.sloth.exception.ServiceUnavailableException;
import org.opendaylight.sloth.service.SlothServiceLocator;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.CheckPermissionInput;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class SlothPermissionActor extends UntypedActor {
    private static final Logger LOG = LoggerFactory.getLogger(SlothPermissionActor.class);
    private SlothReadCache slothReadCache;

    @Override
    public void onReceive(Object o) throws Exception {
        checkSlothReadCache();
        if (o instanceof CheckPermissionInput && slothReadCache != null) {
            LOG.info("SlothPermissionActor receives CheckPermissionInput");
            CheckPermissionInput input = (CheckPermissionInput) o;
            getSender().tell("Got your message: " + this.getSelf(), getSelf());
        } else {
            LOG.warn("SlothPermissionActor receives unknown type message: " + o);
        }
    }

    private void checkSlothReadCache() {
        if (slothReadCache == null) {
            try {
                slothReadCache = SlothServiceLocator.getInstance().getSlothReadCache();
            } catch (ServiceUnavailableException e) {
                e.printStackTrace();
                LOG.error("SlothPermissionActor unable to get SlothReadCache");
            }
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

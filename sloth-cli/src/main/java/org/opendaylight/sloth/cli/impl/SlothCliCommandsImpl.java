/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
package org.opendaylight.sloth.cli.impl;

import org.opendaylight.controller.md.sal.binding.api.DataBroker;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.opendaylight.sloth.cli.api.SlothCliCommands;

public class SlothCliCommandsImpl implements SlothCliCommands {

    private static final Logger LOG = LoggerFactory.getLogger(SlothCliCommandsImpl.class);
    private final DataBroker dataBroker;

    public SlothCliCommandsImpl(final DataBroker db) {
        this.dataBroker = db;
        LOG.info("SlothCliCommandImpl initialized");
    }

    @Override
    public DataBroker getDataBroker() {
        return dataBroker;
    }
}
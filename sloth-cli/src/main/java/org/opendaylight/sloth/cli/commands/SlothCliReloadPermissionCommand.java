/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
package org.opendaylight.sloth.cli.commands;

import org.apache.karaf.shell.commands.Command;
import org.apache.karaf.shell.commands.Option;
import org.apache.karaf.shell.console.AbstractAction;
import org.opendaylight.controller.md.sal.binding.api.DataBroker;
import org.opendaylight.sloth.cli.api.SlothCliCommands;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Command(name = "reload", scope = "sloth", description = "reload permission from configuration file")
public class SlothCliReloadPermissionCommand extends AbstractAction {

    private static final Logger LOG = LoggerFactory.getLogger(SlothCliReloadPermissionCommand.class);
    private static final String PERMISSION_CONFIG_PATH = "./etc/sloth-permission.conf";
    protected final SlothCliCommands service;
    private DataBroker dataBroker;

    public SlothCliReloadPermissionCommand(final SlothCliCommands service) {
        this.service = service;
        LOG.info("SlothCliReloadPermissionCommand initialized");
    }

    @Option(name = "-f", aliases = { "--file" }, description = "file location")
    private String filePath;

    @Override
    protected Object doExecute() throws Exception {
        if (dataBroker == null) {
            dataBroker = service.getDataBroker();
        }
        String path = filePath == null ? PERMISSION_CONFIG_PATH : filePath;
        return "reload permission file success: " + path;
    }
}
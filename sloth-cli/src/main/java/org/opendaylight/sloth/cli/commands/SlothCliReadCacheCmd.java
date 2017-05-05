/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
package org.opendaylight.sloth.cli.commands;


import org.apache.karaf.shell.commands.Command;
import org.apache.karaf.shell.console.AbstractAction;
import org.opendaylight.sloth.cache.SlothReadCache;
import org.opendaylight.sloth.cli.api.SlothCliCommands;
import org.opendaylight.sloth.exception.ServiceUnavailableException;
import org.opendaylight.sloth.service.SlothServiceLocator;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Command(name = "cache", scope = "sloth", description = "read policy cache from memory")
public class SlothCliReadCacheCmd extends AbstractAction {
    private static final Logger LOG = LoggerFactory.getLogger(SlothCliReadCacheCmd.class);
    private final SlothCliCommands service;
    private final SlothReadCache slothReadCache;

    public SlothCliReadCacheCmd(final SlothCliCommands service) throws ServiceUnavailableException {
        this.service = service;
        slothReadCache = SlothServiceLocator.getInstance().getSlothReadCache();
        LOG.info("SlothCliReadCacheCmd initialized");
    }

    @Override
    protected Object doExecute() throws Exception {
        return slothReadCache.toString();
    }
}

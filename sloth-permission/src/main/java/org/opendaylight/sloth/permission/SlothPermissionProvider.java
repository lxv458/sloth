/*
 * Copyright (c) 2017 Northwestern University LIST Group. and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.permission;

import org.opendaylight.controller.md.sal.binding.api.DataBroker;
import org.opendaylight.controller.md.sal.binding.api.NotificationPublishService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * All right reserved.
 * Northwestern University LIST Lab 2017.
 * Created by libin on 17-1-27.
 */
public class SlothPermissionProvider {
    private final static Logger LOG = LoggerFactory.getLogger(SlothPermissionProvider.class);

    private final DataBroker dataBroker;
    private final NotificationPublishService notificationPublishService;


    public SlothPermissionProvider(final DataBroker dataBroker,
                                   final NotificationPublishService notificationPublishService) {
        this.dataBroker = dataBroker;
        this.notificationPublishService = notificationPublishService;
    }

    public void init() {
    }

    public void close() throws Exception {
    }
}

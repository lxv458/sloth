/*
 * Copyright (c) 2017 Northwestern University LIST Group. and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.web;

import javax.ws.rs.core.Application;
import java.util.HashSet;
import java.util.Set;

/**
 * All right reserved.
 * Northwestern University LIST Lab 2017.
 * Created by libin on 17-1-27.
 */
public class SlothNorthboundApplication extends Application {
    @Override
    public Set<Class<?>> getClasses() {
        Set<Class<?>> set = new HashSet<>();
        set.add(SlothNorthbound.class);
        return set;
    }
}

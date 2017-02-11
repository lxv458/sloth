/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
package org.opendaylight.sloth.northbound;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;

@XmlRootElement
@XmlAccessorType(XmlAccessType.NONE)
public class SlothNetworkRequest {
    @XmlElement(name = "network")
    SlothNetwork network;

    SlothNetworkRequest() {}

    public SlothNetworkRequest(SlothNetwork network) {
        this.network = network;
    }

    public SlothNetwork getNetwork() {
        return network;
    }

    public void setNetwork(SlothNetwork network) {
        this.network = network;
    }


}

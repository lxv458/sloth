/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
package org.opendaylight.sloth.northbound;

import javax.ws.rs.Consumes;
import javax.ws.rs.DELETE;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.PUT;
import javax.ws.rs.Path;
import javax.ws.rs.PathParam;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.net.HttpURLConnection;


@Path("/sloth")
public class SlothNorthboundImpl {
    @Path("{network_id}")
    @GET
    @Produces({MediaType.APPLICATION_JSON})
    public Response getData(@PathParam("network_id") String networkId) {
        return Response.status(HttpURLConnection.HTTP_OK).entity(new SlothNetworkRequest(SlothNetwork.getSampleSlothNetwork())).build();
    }

    @Path("{network_id}")
    @PUT
    @Consumes({MediaType.APPLICATION_JSON})
    @Produces({MediaType.APPLICATION_JSON})
    public Response putData(@PathParam("network_id") String networkId) {
        return Response.status(HttpURLConnection.HTTP_OK).entity(new SlothNetworkRequest(SlothNetwork.getSampleSlothNetwork())).build();
    }

    @POST
    @Consumes({MediaType.APPLICATION_JSON})
    @Produces({MediaType.APPLICATION_JSON})
    public Response postData() {
        return Response.status(HttpURLConnection.HTTP_OK).entity(new SlothNetworkRequest(SlothNetwork.getSampleSlothNetwork())).build();
    }

    @Path("{network_id}")
    @DELETE
    @Produces({MediaType.APPLICATION_JSON})
    public Response deleteData(@PathParam("network_id") String networkId) {
        return Response.status(HttpURLConnection.HTTP_OK).entity(new SlothNetworkRequest(SlothNetwork.getSampleSlothNetwork())).build();
    }
}

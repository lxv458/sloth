/*
 * Copyright (c) 2017 Northwestern University LIST Group. and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.web;

import javax.ws.rs.DELETE;
import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.PUT;
import javax.ws.rs.Path;
import javax.ws.rs.Produces;
import javax.ws.rs.core.MediaType;
import javax.ws.rs.core.Response;
import java.net.HttpURLConnection;

/**
 * All right reserved.
 * Northwestern University LIST Lab 2017.
 * Created by libin on 17-1-27.
 */


@Path("/sloth")
public class SlothNorthbound {
    @GET
    @Produces({MediaType.APPLICATION_JSON})
    public Response getData() {
        return Response.status(HttpURLConnection.HTTP_OK).entity("Hello World!").build();
    }

    @PUT
    @Produces({MediaType.APPLICATION_JSON})
    public Response putData() {
        return Response.status(HttpURLConnection.HTTP_OK).build();
    }

    @POST
    @Produces({MediaType.APPLICATION_JSON})
    public Response postData() {
        return Response.status(HttpURLConnection.HTTP_OK).build();
    }

    @DELETE
    @Produces({MediaType.APPLICATION_JSON})
    public Response deleteData() {
        return Response.status(HttpURLConnection.HTTP_OK).build();
    }
}

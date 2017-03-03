/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.cache.model;


import com.jayway.jsonpath.Configuration;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.HttpType;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.check.permission.input.Request;

import java.util.LinkedHashMap;
import java.util.Map;

public class SlothRequest {
    private final String requestUrl;
    private final HttpType method;
    private final Map<String, String> queryString;
    private final Object document;

    public SlothRequest(Request request) {
        requestUrl = request.getRequestUrl();
        method = request.getMethod();
        queryString = splitQuery(request.getQueryString());
        document = Configuration.defaultConfiguration().jsonProvider().parse(request.getJsonBody());
    }

    private static Map<String, String> splitQuery(String queryString) {
        Map<String, String> queryPairs = new LinkedHashMap<>();
        String[] pairs = queryString.split("&");
        for (String pair : pairs) {
            int idx = pair.indexOf("=");
            queryPairs.put(pair.substring(0, idx), pair.substring(idx + 1));
        }
        return queryPairs;
    }

    public String getRequestUrl() {
        return requestUrl;
    }

    public HttpType getMethod() {
        return method;
    }

    public Map<String, String> getQueryString() {
        return queryString;
    }

    public Object getDocument() {
        return document;
    }
}

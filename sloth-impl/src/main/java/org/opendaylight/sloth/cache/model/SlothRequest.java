/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.cache.model;


import com.jayway.jsonpath.JsonPath;
import com.jayway.jsonpath.ReadContext;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.CheckPermissionInput;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.HttpType;

import java.util.LinkedHashMap;
import java.util.Map;

public class SlothRequest {
    private final String requestUrl;
    private final HttpType method;
    private final Map<String, String> queryString;
    private final ReadContext readContext;

    public SlothRequest(CheckPermissionInput input) {
        requestUrl = input.getRequest().getRequestUrl();
        method = input.getRequest().getMethod();
        queryString = splitQuery(input.getRequest().getQueryString());
        readContext = input.getRequest().getJsonBody() != null && !input.getRequest().getJsonBody().isEmpty() ?
                JsonPath.parse(input.getRequest().getJsonBody()) : null;
    }

    private static Map<String, String> splitQuery(String queryString) {
        Map<String, String> queryPairs = new LinkedHashMap<>();
        if (queryString != null && !queryString.isEmpty()) {
            for (String pair : queryString.split("&")) {
                int idx = pair.indexOf("=");
                queryPairs.put(pair.substring(0, idx), pair.substring(idx + 1));
            }
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

    public ReadContext getReadContext() {
        return readContext;
    }
}

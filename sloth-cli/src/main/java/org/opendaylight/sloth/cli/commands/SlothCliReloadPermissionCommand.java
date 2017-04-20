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
import org.json.JSONArray;
import org.json.JSONObject;
import org.opendaylight.controller.md.sal.binding.api.DataBroker;
import org.opendaylight.controller.md.sal.binding.api.WriteTransaction;
import org.opendaylight.controller.md.sal.common.api.data.LogicalDatastoreType;
import org.opendaylight.controller.md.sal.common.api.data.TransactionCommitFailedException;
import org.opendaylight.sloth.cli.api.SlothCliCommands;
import org.opendaylight.sloth.policy.SlothPolicyFileParser;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.Domains;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.DomainsBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.Permissions;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.PermissionsBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.SlothPolicyHub;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.domains.Domain;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.domains.DomainBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.domains.domain.Role;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.domains.domain.RoleBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.permissions.Permission;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.permissions.PermissionBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.permissions.permission.ParamJson;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.permissions.permission.ParamJsonBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.permissions.permission.ParamQuery;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.model.rev150105.permissions.permission.ParamQueryBuilder;
import org.opendaylight.yang.gen.v1.urn.opendaylight.sloth.permission.rev150105.HttpType;
import org.opendaylight.yangtools.yang.binding.InstanceIdentifier;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.UUID;
import java.util.regex.Pattern;

@Command(name = "reload", scope = "sloth", description = "reload permission from configuration file")
public class SlothCliReloadPermissionCommand extends AbstractAction {
    private static final Logger LOG = LoggerFactory.getLogger(SlothCliReloadPermissionCommand.class);
    private static final String PERMISSION_CONFIG_PATH = "./etc/sloth-permission.conf";
    private static final String POLICY_FILE_PATH = "./etc/sloth-policy";
    private static final InstanceIdentifier<Domains> SLOTH_DOMAINS_ID = InstanceIdentifier.create(Domains.class);
    private static final InstanceIdentifier<Permissions> SLOTH_PERMISSIONS_ID = InstanceIdentifier.create(Permissions.class);
    private static final InstanceIdentifier<SlothPolicyHub> SLOTH_POLICY_HUB_ID = InstanceIdentifier.create(SlothPolicyHub.class);

    private final SlothCliCommands service;
    private DataBroker dataBroker;
    @Option(name = "-f", aliases = {"--file"}, description = "file location")
    private String filePath;

    public SlothCliReloadPermissionCommand(final SlothCliCommands service) {
        this.service = service;
        LOG.info("SlothCliReloadPermissionCommand initialized");
    }

    @Override
    protected Object doExecute() throws Exception {
        if (dataBroker == null) {
            dataBroker = service.getDataBroker();
        }
        String path = filePath == null ? PERMISSION_CONFIG_PATH : filePath;
        if (clearDataStore()) {
            SlothPolicyHub slothPolicyHub = new SlothPolicyFileParser(POLICY_FILE_PATH).parse();
            JSONObject jsonObject = loadPermission(path);
            List<Domain> domainList = new ArrayList<>();
            List<Permission> permissionList = new ArrayList<>();
            extractDomainAndPermission(jsonObject, domainList, permissionList);
            if (writeDataStore(domainList, permissionList, slothPolicyHub)) {
                return jsonObject.toString(4);
            } else {
                return "failed to write data store. reload stopped";
            }
        } else {
            return "failed to clear data store. reload stopped";
        }
    }

    private static JSONObject loadPermission(String path) throws Exception {
        BufferedReader reader = null;
        String jsonData = "";
        try {
            String line;
            reader = new BufferedReader(new FileReader(path));
            while ((line = reader.readLine()) != null) {
                line = line.trim();
                if (!line.startsWith("#")) {
                    jsonData += line;
                }
            }
        } catch (FileNotFoundException e) {
            LOG.error("failed to open file: " + path);
        } catch (IOException e) {
            LOG.error("failed to read file: " + path);
        } finally {
            if (reader != null) {
                try {
                    reader.close();
                } catch (IOException e) {
                    LOG.error("failed to close file: " + path);
                }
            }
        }
        JSONObject jsonObject = new JSONObject(jsonData);
        Map<String, String> marcoMap = getMarcoMap(jsonObject);
        for (Map.Entry<String, String> entry : marcoMap.entrySet()) {
            jsonData = jsonData.replaceAll(Pattern.quote(String.format("${%s}", entry.getKey())), entry.getValue());
        }
        return new JSONObject(jsonData);
    }

    private static Map<String, String> getMarcoMap(JSONObject root) throws Exception {
        JSONObject jsonObject = root.getJSONObject("marcos");
        Map<String, String> marcoMap = new HashMap<>();
        Iterator<?> keys = jsonObject.keys();
        while (keys.hasNext()) {
            String key = (String) keys.next();
            if (key.indexOf('$') >= 0) {
                throw new Exception("marcos name should not contain replacement");
            }
            Object object = jsonObject.get(key);
            if (object instanceof String) {
                marcoMap.put(key, (String) object);
            } else {
                throw new Exception("marcos contain none string content");
            }
        }
        Map<String, String> result = new HashMap<>(), mid = new HashMap<>(), tmp = new HashMap<>();
        while (!marcoMap.isEmpty()) {
            mid.clear();
            tmp.clear();
            for (Map.Entry<String, String> entry : marcoMap.entrySet()) {
                if (entry.getValue().indexOf('$') < 0) {
                    mid.put(entry.getKey(), entry.getValue());
                } else {
                    tmp.put(entry.getKey(), entry.getValue());
                }
            }
            marcoMap.clear();
            for (Map.Entry<String, String> entry : tmp.entrySet()) {
                String value = entry.getValue();
                for (Map.Entry<String, String> e : mid.entrySet()) {
                    value = value.replaceAll(Pattern.quote(String.format("${%s}", e.getKey())), e.getValue());
                }
                marcoMap.put(entry.getKey(), value);
            }
            result.putAll(mid);
        }
        return result;
    }

    private static void extractDomainAndPermission(JSONObject jsonObject, List<Domain> domainList, List<Permission> permissionList) {
        Map<String, String> permissionNameToId = new HashMap<>();
        JSONArray permissions = jsonObject.getJSONArray("permissions");
        for (int k = 0; k < permissions.length(); k++) {
            JSONObject permission = permissions.getJSONObject(k);
            PermissionBuilder permissionBuilder = new PermissionBuilder();
            permissionBuilder.setId(permission.optString("id").isEmpty() ? UUID.randomUUID().toString() : permission.getString("id"))
                    .setName(permission.getString("name"))
                    .setResource(jsonArrayToStringList(permission.getJSONArray("resources")))
                    .setAction(jsonArrayToHttpTypeList(permission.getJSONArray("actions")))
                    .setDisabled(permission.optBoolean("disabled"))
                    .setParamQuery(jsonArrayToParamQueryList(permission.optJSONArray("param_query")))
                    .setParamJson(jsonArrayToParamJsonList(permission.optJSONArray("param_json")));
            permissionList.add(permissionBuilder.build());
            permissionNameToId.put(permissionBuilder.getName(), permissionBuilder.getId());
        }

        JSONArray domains = jsonObject.getJSONArray("domains");
        for (int i = 0; i < domains.length(); i++) {
            JSONObject domain = domains.getJSONObject(i);
            DomainBuilder domainBuilder = new DomainBuilder();
            domainBuilder.setId(domain.optString("id").isEmpty() ? UUID.randomUUID().toString() : domain.getString("id"))
                    .setName(domain.getString("name"))
                    .setDisabled(domain.optBoolean("disabled"));
            List<Role> roleList = new ArrayList<>();
            JSONArray roles = domain.getJSONArray("roles");
            for (int j = 0; j < roles.length(); j++) {
                JSONObject role = roles.getJSONObject(j);
                RoleBuilder roleBuilder = new RoleBuilder();
                roleBuilder.setId(role.optString("id").isEmpty() ? UUID.randomUUID().toString() : role.getString("id"))
                        .setName(role.getString("name"))
                        .setPriority(role.getInt("priority"))
                        .setDisabled(role.optBoolean("disabled"));
                List<String> permissionIdList = new ArrayList<>();
                for (String name : jsonArrayToStringList(role.getJSONArray("permissions"))) {
                    permissionIdList.add(permissionNameToId.get(name));
                }
                roleBuilder.setPermissionId(permissionIdList);
                roleList.add(roleBuilder.build());
            }
            domainBuilder.setRole(roleList);
            domainList.add(domainBuilder.build());
        }
    }

    private static List<HttpType> jsonArrayToHttpTypeList(JSONArray jsonArray) {
        List<HttpType> result = new ArrayList<>();
        for (int i = 0; i < jsonArray.length(); i++) {
            result.add(HttpType.valueOf(jsonArray.getString(i)));
        }
        return result;
    }

    private static List<String> jsonArrayToStringList(JSONArray jsonArray) {
        List<String> result = new ArrayList<>();
        for (int i = 0; i < jsonArray.length(); i++) {
            result.add(jsonArray.getString(i));
        }
        return result;
    }

    private static List<ParamQuery> jsonArrayToParamQueryList(JSONArray jsonArray) {
        List<ParamQuery> paramQueryList = new ArrayList<>();
        if (jsonArray != null) {
            for (int i = 0; i < jsonArray.length(); i++) {
                ParamQueryBuilder paramQueryBuilder = new ParamQueryBuilder();
                JSONObject paramQuery = jsonArray.getJSONObject(i);
                paramQueryBuilder.setParam(paramQuery.getString("param"))
                        .setValue(jsonArrayToStringList(paramQuery.getJSONArray("value")));
                paramQueryList.add(paramQueryBuilder.build());
            }
        }
        return paramQueryList;
    }

    private static List<ParamJson> jsonArrayToParamJsonList(JSONArray jsonArray) {
        List<ParamJson> paramJsonList = new ArrayList<>();
        if (jsonArray != null) {
            for (int i = 0; i < jsonArray.length(); i++) {
                ParamJsonBuilder paramJsonBuilder = new ParamJsonBuilder();
                JSONObject paramJson = jsonArray.getJSONObject(i);
                paramJsonBuilder.setParam(paramJson.getString("param"))
                        .setValue(jsonArrayToStringList(paramJson.getJSONArray("value")));
                paramJsonList.add(paramJsonBuilder.build());
            }
        }
        return paramJsonList;
    }

    private boolean clearDataStore() {
        try {
            WriteTransaction wtx = dataBroker.newWriteOnlyTransaction();
            wtx.delete(LogicalDatastoreType.CONFIGURATION, SLOTH_POLICY_HUB_ID);
            wtx.delete(LogicalDatastoreType.CONFIGURATION, SLOTH_DOMAINS_ID);
            wtx.delete(LogicalDatastoreType.CONFIGURATION, SLOTH_PERMISSIONS_ID);
            wtx.submit().checkedGet();
        } catch (TransactionCommitFailedException e) {
            LOG.error("failed to delete permissions and domains from data store: " + e.getMessage());
            return false;
        }
        return true;
    }

    private boolean writeDataStore(List<Domain> domainList, List<Permission> permissionList, SlothPolicyHub slothPolicyHub) {
        try {
            WriteTransaction wtx = dataBroker.newWriteOnlyTransaction();
            DomainsBuilder domainsBuilder = new DomainsBuilder();
            domainsBuilder.setDomain(domainList);
            PermissionsBuilder permissionsBuilder = new PermissionsBuilder();
            permissionsBuilder.setPermission(permissionList);
            wtx.put(LogicalDatastoreType.CONFIGURATION, SLOTH_DOMAINS_ID, domainsBuilder.build(), true);
            wtx.put(LogicalDatastoreType.CONFIGURATION, SLOTH_PERMISSIONS_ID, permissionsBuilder.build(), true);
            wtx.put(LogicalDatastoreType.CONFIGURATION, SLOTH_POLICY_HUB_ID, slothPolicyHub, true);
            wtx.submit().checkedGet();
        } catch (TransactionCommitFailedException e) {
            LOG.error("failed to write permissions and domains into data store: " + e.getMessage());
            return false;
        }
        return true;
    }

}
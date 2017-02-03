/*
 * Copyright (c) 2017 Northwestern University LIST Group. and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */

package org.opendaylight.sloth.web;

import javax.xml.bind.annotation.XmlAccessType;
import javax.xml.bind.annotation.XmlAccessorType;
import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.UUID;

/**
 * All right reserved.
 * Northwestern University LIST Lab 2017.
 * Created by libin on 17-1-31.
 */
@XmlRootElement
@XmlAccessorType(XmlAccessType.NONE)
public class SlothNetwork implements Serializable {
    @XmlElement(name = "status")
    String status;

    @XmlElement(namespace = "router", name = "external")
    Boolean routerExternal;

    @XmlElement(name = "availability_zone_hints")
    List<String> availabilityZoneHints;

    @XmlElement(name = "availability_zones")
    List<String> availabilityZones;

    @XmlElement(name = "name")
    String name;

    @XmlElement(name = "admin_state_up")
    Boolean adminStateUp;

    @XmlElement(name = "tenant_id")
    String tenantId;

    @XmlElement(name = "project_id")
    String projectId;

    @XmlElement(name = "updated_at")
    String updatedAt;

    @XmlElement(name = "changed_at")
    String changedAt;

    @XmlElement(name = "mtu")
    Integer mtu;

    @XmlElement(name = "qos_policy_id")
    String qosPolicyId;

    @XmlElement(name = "subnets")
    List<String> subnets;

    @XmlElement(name = "shared")
    Boolean shared;

    @XmlElement(name = "id")
    String id;

    SlothNetwork() {}

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {
        this.status = status;
    }

    public Boolean getRouterExternal() {
        return routerExternal;
    }

    public void setRouterExternal(Boolean routerExternal) {
        this.routerExternal = routerExternal;
    }

    public List<String> getAvailabilityZoneHints() {
        return availabilityZoneHints;
    }

    public void setAvailabilityZoneHints(List<String> availabilityZoneHints) {
        this.availabilityZoneHints = availabilityZoneHints;
    }

    public List<String> getAvailabilityZones() {
        return availabilityZones;
    }

    public void setAvailabilityZones(List<String> availabilityZones) {
        this.availabilityZones = availabilityZones;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Boolean getAdminStateUp() {
        return adminStateUp;
    }

    public void setAdminStateUp(Boolean adminStateUp) {
        this.adminStateUp = adminStateUp;
    }

    public String getTenantId() {
        return tenantId;
    }

    public void setTenantId(String tenantId) {
        this.tenantId = tenantId;
    }

    public String getProjectId() {
        return projectId;
    }

    public void setProjectId(String projectId) {
        this.projectId = projectId;
    }

    public String getUpdatedAt() {
        return updatedAt;
    }

    public void setUpdatedAt(String updatedAt) {
        this.updatedAt = updatedAt;
    }

    public String getChangedAt() {
        return changedAt;
    }

    public void setChangedAt(String changedAt) {
        this.changedAt = changedAt;
    }

    public Integer getMtu() {
        return mtu;
    }

    public void setMtu(Integer mtu) {
        this.mtu = mtu;
    }

    public String getQosPolicyId() {
        return qosPolicyId;
    }

    public void setQosPolicyId(String qosPolicyId) {
        this.qosPolicyId = qosPolicyId;
    }

    public List<String> getSubnets() {
        return subnets;
    }

    public void setSubnets(List<String> subnets) {
        this.subnets = subnets;
    }

    public Boolean getShared() {
        return shared;
    }

    public void setShared(Boolean shared) {
        this.shared = shared;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    @Override
    public String toString() {
        return "Network [" +
                "status=" + status +
                ", router:external=" + routerExternal +
                ", availability_zone_hints=" + availabilityZoneHints +
                ", availability_zones=" + availabilityZones +
                ", name=" + name +
                ", admin_state_up=" + adminStateUp +
                ", tenant_id=" + tenantId +
                ", project_id=" + projectId +
                ", updated_at=" + updatedAt +
                ", changed_at=" + changedAt +
                ", mtu=" + mtu +
                ", qos_policy_id=" + qosPolicyId +
                ", subnets=" + subnets +
                ", shared=" + shared +
                ", id=" + id + "]";
    }

    static public SlothNetwork getSampleSlothNetwork() {
        SlothNetwork slothNetwork = new SlothNetwork();
        slothNetwork.setStatus("ACTIVE");
        slothNetwork.setRouterExternal(false);
        slothNetwork.setAvailabilityZoneHints(new ArrayList<>());
        slothNetwork.setAvailabilityZones(new ArrayList<>());
        slothNetwork.setName("sloth-sample-network-0.4.0-Boron");
        slothNetwork.setAdminStateUp(true);
        slothNetwork.setTenantId(UUID.randomUUID().toString());
        slothNetwork.setProjectId(UUID.randomUUID().toString());
        slothNetwork.setUpdatedAt(new Date().toString());
        slothNetwork.setChangedAt(new Date().toString());
        slothNetwork.setMtu(1440);
        slothNetwork.setQosPolicyId(UUID.randomUUID().toString());
        slothNetwork.setSubnets(new ArrayList<>());
        slothNetwork.setShared(false);
        slothNetwork.setId(UUID.randomUUID().toString());
        return slothNetwork;
    }
}

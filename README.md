# Sloth Security Filter

![Sloth](http://kids.nationalgeographic.com/content/dam/kids/photos/animals/Mammals/Q-Z/sloth-beach-upside-down.jpg.adapt.945.1.jpg)

Author: Libin Song, Northwestern University

`Sloth Security Filter` is a light weight Java Servlet Filter with backend data store support, designed for OpenDaylight controller. It provides fine grained role based access control on generic RESTful API services. It also support runtime configuration and can be deployed distributedly. And it is easy to install and 100% compatible with existing AAA project. You don't need to change any things on existing OpenDaylight projects.

## Installation

1. Add `Sloth` as a CustomFilter
	* [Dynamic Filter Injection](https://wiki.opendaylight.org/view/AAA:DynamicFilterFramework)
2. Start `Sloth` feature in Karaf command line

## Feature

`Sloth` is a [Java Servlet Filter](https://docs.oracle.com/cd/B14099_19/web.1012/b14017/filters.htm). A Servlet Filter is able to filter before and after API is processed. `Sloth` will check parameters both before and after API processing, blocking malicious API request and filtering out unprivileged content. For example, administrators can set permissions to restrict the network type and IP range for creation. And the response can also be filtered, if user is requesting resources of others.


## Configuration

`Sloth` has a Json based configuration file, which is extremely for programmers or administrators to write fine grained access control for generic RESTful API. The configuration file is located at `/etc/sloth-permission.conf`. `sloth-permission.conf` file can be imported via karaf command line `sloth:reload` or you can reload from other configuration files, e.g. `sloth:reload /etc/sloth-permission.conf` which is saying `Sloth` is able to reload configuration at any time from any where. The following is an example configuration file.

```bash
# comment is supported
# only '#' is supported as comment
# '#' should be at the begining of comment line
{
  # "marcos" is a predefined field, which is used for
  # alias definition. Configuration interpretor will
  # replace those marcos during interpretation.
  # left side is the name of variables that will be
  # replaced, and right side is the value. Left side
  # replacement is prohibited, since name should be
  # neat and clean. Of course, marcos can be empty.
  # of course, marcos can be empty
  "marcos": {
    "api_v2": "/v2.0",
    "extensions": "${api_v2}/extensions",
    "networks": "${api_v2}/networks",
    "ports": "${api_v2}/ports",
    "segments": "${api_v2}/segments",
    "trunks": "${api_v2}/trucks",
    "floatingips": "${api_v2}/floatingips",
    "routers": "${api_v2}/routers",
    "subnetpools": "${api_v2}/subnetpools",
    "subnets": "${api_v2}/subnets"
  },
  # domain in RBAC (role based access control)
  "domains": [
    {
      # "id" optional. If not provide, interpretor
      # will generate "id" with Java UUID
      "id": "2ac336d2-1ebc-4dc7-af68-2789e6c9b7c0",
      # "name", name of domain in in RBAC
      "name": "sdn",
      # if domain is disabled, default false
      "disabled": false,
      # "roles", exactly the same as that in RBAC
      "roles": [
        {
          # "id" oprional.
          "id": "29d953f7-e1a8-4251-bfc5-006b799d5d34",
          # "name", name of role in RBAC
          "name": "admin",
          # priority of role, in permission check
          # permission will check roles in descending order
          "priority": 0,
          # if role is disabled, default false
          "disabled": false,
          # "permissions" required.
          "permissions": ["p1"]
        }, {
          "id": "5a9a123d-ea53-484b-8529-877fc8156908",
          "name": "user",
          "priority": 1,
          "disabled": false,
          "permissions": ["p2", "p3"]
        }
      ]
    }
  ],
  "permissions": [
    {
      "name": "p1",
      # "id" optional
      "id": "ea945536-df20-4e0d-840a-cc1a757c2e72",
      # if permission is disabled
      "disabled": false,
      # "resources", will be matched by regular expression.
      # Only resources listed here are valid for further
      # checking.
      "resources": ["${networks}", "${ports}", "${segments}"],
      # "actions" HTTP Method. Only Method listed
      # here are valid for further checking.
      "actions": ["POST", "GET", "PUT", "DELETE"],
      # "param_query", restrictions on the query parameters
      # after the "?" mark in URL
      "param_query": [],
      # "param_json", restrictions on the json data
      "param_json": []
    }, {
      "name": "p2",
      "id": "2df79cf9-226a-4858-9fe0-b5319094a121",
      "resources": ["${networks}"],
      "actions": ["POST", "GET", "PUT", "DELETE"]
    }, {
      "name": "p3",
      "id": "93d581ed-55bc-49b2-a0ff-230ce5573993",
      "resources": ["${networks}"],
      "actions": ["POST"],
      "param_query": [],
      "param_json": [
        {
          # URL pattern param, specifying parameter in Json
          "param": "/network/provider:network_type",
          # oerator can be "ENUM", "REGEX", "RANGE"
          "operator": "ENUM",
          "value": ["vlan"]
        }, {
          # double slash "//" means list in Json
          "param": "/network/segments//provider:network_type",
          "operator": "ENUM",
          "value": ["stt"]
        }
      ]
    }
  ]
}
```

## Note

1. Currently, we are using 1.3.0-SNAPSHOT opendaylight-startup-archetype.

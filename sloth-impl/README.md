- REST Requset is filtered by filter.SlothSecurityFilter -> doFilter

- doFilter Call SlothPermissionEngine.checkPermission

- SlothPermissionEngine.checkPermission -> permissionRouter(SlothPermissionRouter) Where Number of Routee is 10

@TODO: How about we change Number of Routee to a large number?

- SlothPermissionRouter create some SlothPermissionActor

- SlothPermissionRoute.onReceive -> route to SlothPermissionActor

(Props is a ActorRef configuration object, that is thread safe and fully sharable. Used when creating new actors through;)

- SlothPermissionActor.onReceive ->slothReadCache.policyCheck(input)

- ##修改这里##

- slothReadCache.policyCheck

-- globalPolicyCache.policyCheck(slothRequest)

---- Map.Entry<String, Policy> entry : globalPolicyCache.asMap().entrySet()
---- CheckResult r = entry.getValue().Check(input);

-- localPolicyCache.policyCheck(slothRequest)

---- Cache<String, Policy> value = localPolicyCache.getIfPresent(key);
---- Map.Entry<String, Policy> entry : value.asMap().entrySet()
---- CheckResult r = entry.getValue().Check(input);

- Then, we got a result at slothReadCache.policyCheck

- Return to SlothPermissionEngine.checkPermission

- Build a RpcResult and Return to SlothSecurityFilter
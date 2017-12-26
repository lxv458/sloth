### defined two cli commands

#### sloth:cache

slothReadCache = SlothServiceLocator.getInstance().getSlothReadCache();

return slothReadCache.toString();

#### sloth:reload

Option -f --file

> PERMISSION_CONFIG_PATH = "./etc/sloth-permission.conf";  
> POLICY_FILE_PATH = "./etc/sloth-policy";

file sloth-permission.conf is located at sloth-impl/src/main/resources/sloth-permission.conf

But I cannot understand what the file means. This file is used by "writeDataStore" function in sloth:reload
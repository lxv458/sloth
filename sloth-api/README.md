API feature has only two YANG files.
Which define the data model used in sloth.

sloth-permission file descripes the information in REST request.

sloth-model file descripes the componet in policy.
It refers sloth-permission file. 

@TODO: in sloth-model, the defination of local policy set is need to update.

    container sloth-policy-hub {
        container global-policy-set {
            uses policies;
        }
        list local-policy-set {
            key "id";
            leaf id {
                type string;
            }
            uses policies;
        }
    }

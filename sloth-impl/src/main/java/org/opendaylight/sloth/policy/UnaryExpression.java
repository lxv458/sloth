/*
 * Copyright © 2016 Northwestern University LIST Lab, Libin Song and others.  All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v1.0 which accompanies this distribution,
 * and is available at http://www.eclipse.org/legal/epl-v10.html
 */
package org.opendaylight.sloth.policy;


import org.opendaylight.sloth.cache.model.SlothRequest;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

public class UnaryExpression implements Expression {
    /*
    * The value here is defined as object.
    * It should be casted to actual value, according to ElementType.
    * Here is the mapping:
    * ElementType.NULL                  =>     null
    * ElementType.FLOAT                 =>     Float
    * ElementType.STRING                =>     String
    * ElementType.BOOLEAN               =>     Boolean
    * ElementType.JSON_PATH             =>     String
    * ElementType.SLOTH_PREDEFINED      =>     SlothPredefined
    *
    * SlothPredefined is for extensibility.
    * */
    private final Object value;
    private final ElementType elementType;

    public UnaryExpression(Object value, ElementType elementType) {
        this.value = value;
        this.elementType = elementType;
    }

    @Override
    public ExprValue Evaluate(SlothRequest input) {
        Object v;
        ElementType t;
        switch (elementType) {
            case JSON_PATH:
                v = input.getReadContext().read((String) value);
                if (v == null) {
                    v = "null";
                    t = ElementType.NULL;
                } else if (v instanceof String) {
                    t = ElementType.STRING;
                } else if (v instanceof Integer) {
                    v = ((Integer) v).floatValue();
                    t = ElementType.FLOAT;
                } else if (v instanceof Double) {
                    v = ((Double) v).floatValue();
                    t = ElementType.FLOAT;
                } else if (v instanceof Boolean) {
                    t = ElementType.BOOLEAN;
                } else if (v instanceof List) {
                    if (((List) v).isEmpty()) {
                        t = ElementType.EMPTY_LIST;
                    } else {
                        Object x = null;
                        for (Object xx : (List) v) {
                            if (xx != null) {
                                x = xx;
                                break;
                            }
                        }
                        if (x == null) {
                            t = ElementType.EMPTY_LIST;
                        } else if (x instanceof String) {
                            //TODO: not sure if we need to further transform it to ArrayList<String>
                            t = ElementType.STRING_LIST;
                        } else if (x instanceof Integer) {
                            //TODO: not sure if we need to further transform it to ArrayList<Float>
                            t = ElementType.FLOAT_LIST;
                        } else if (x instanceof Double) {
                            //TODO: not sure if we need to further transform it to ArrayList<Float>
                            t = ElementType.FLOAT_LIST;
                        } else {
                            throw new IllegalArgumentException("too complex data structure parsed!");
                        }
                    }
                } else {
                    throw new IllegalArgumentException("unknown json path data parsed!");
                }
                break;
            case SLOTH_PREDEFINED:
                t = ElementType.STRING;
                switch ((SlothPredefined) value) {
                    case SLOTH_SUBJECT_ROLE:
                        //TODO: a user can have multiple roles, now we only use one of them
                        v = input.getRoles().get(0);
                        break;
                    case SLOTH_SUBJECT_USER_ID:
                        v = input.getUserId();
                        break;
                    case SLOTH_ACTION_URL:
                        v = input.getRequestUrl();
                        break;
                    case SLOTH_ACTION_METHOD:
                        v = input.getMethod().getName();
                        break;
                    case SLOTH_ACTION_QUERY_STRING:
                        //TODO: implement query string
                        v = "query string has not been implemented";
                        break;
                    case SLOTH_ENVIRONMENT_DATE:
                        v = new SimpleDateFormat("yyyy-MM-dd").format(new Date());
                        break;
                    case SLOTH_ENVIRONMENT_TIME:
                        v = new SimpleDateFormat("HH:mm:ss").format(new Date());
                        break;
                    case SLOTH_ENVIRONMENT_DAY_OF_WEEK:
                        v = new SimpleDateFormat("E").format(new Date());
                        break;
                    default:
                        throw new IllegalArgumentException("unknown sloth predefined type");
                }
                break;
            default:
                v = value;
                t = elementType;
                break;
        }
        return new ExprValue(v, t);
    }

    @Override
    public String toString() {
        return value instanceof SlothPredefined ? ((SlothPredefined) value).getName() : value.toString();
    }
}

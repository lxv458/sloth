grammar SlothPolicy;
r   : 'hello' ID;
ID  : [a-z]+ ;


WHITESPACE  : [ \t\r\n\u000C]+ -> skip;

COMMENT : '/*' .*? '*/' -> skip;

LINE_COMMENT : '//' ~[\r\n]* -> skip;


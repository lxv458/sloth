grammar SlothPolicyRule;

policySet : globalPolicySet? localPolicySet?;

globalPolicySet : 'GLOBAL_POLICY' '{' policyStatement* '}';

localPolicySet : 'LOCAL_POLICY' '{' localPolicyStatement* '}';

localPolicyStatement : Identifier ',' Identifier '{' policyStatement* '}';

policyStatement : Identifier statement;

statement
    :   '{' statement '}'
    |   'ACCEPT'
    |   'REJECT'
    |   'if' '(' expression ')' statement ('else' statement)?
    ;

expression
    :   primary
    |   '(' expression ')'
    |   expression operator expression
    ;

operator
    : '<=' | '>=' | '>' | '<' | '==' | '!=' | '&&' | '||' | 'REG'
    ;

primary
    :   jsonpath
    |   slothPredefined
    |   literal
    ;

jsonpath : '$.' dotExpression ('.' dotExpression)*;

dotExpression : identifierWithQualifier | Identifier;

identifierWithQualifier
    : Identifier '[]'
    | Identifier '[' IntegerLiteral ']'
    | Identifier '[?(' queryExpression ')]'
    ;

queryExpression
    :   queryExpression ('&&' queryExpression)+
    |   queryExpression ('||' queryExpression)+
    |   '*'
    |   '@.' Identifier
    |   '@.' Identifier '>' IntegerLiteral
    |   '@.' Identifier '<' IntegerLiteral
    |   '@.length-' IntegerLiteral
    |   '@.' Identifier '==' IntegerLiteral
    |   '@.' Identifier '==\'' IntegerLiteral '\''
    ;

slothPredefined
    :   'sloth.subject.' ('role' | 'user_id')
    |   'sloth.action.' ('method' | 'url' | 'query_string')
    |   'sloth.environment.' ('date' | 'time' | 'day_of_week')
    ;

literal
    :   IntegerLiteral
    |   FloatingPointLiteral
    |   StringLiteral
    |   BooleanLiteral
    |   NullLiteral
    ;

IntegerLiteral : NonzeroDigit Digit*;

FloatingPointLiteral : Digit* '.' Digit*;

StringLiteral : '"' SingleCharacter+ '"';

BooleanLiteral : 'true' | 'false';

NullLiteral : 'null';

fragment
NonzeroDigit : [1-9];

fragment
Digit : [0-9];

fragment
SingleCharacter : ~["\\];



GLOBAL_POLICY : 'GLOBAL_POLICY';
LOCAL_POLICY : 'LOCAL_POLICY';
ACCEPT : 'ACCEPT';
REJECT : 'REJECT';
LBRACE : '{';
RBRACE : '}';
IF : 'if';
ELSE : 'else';
EQUAL : '==';
NOTEQUAL : '!=';
LT : '<';
GT : '>';
LE : '<=';
GE : '>=';
AND : '&&';
OR : '||';
REGULAR : 'REG';




Identifier :Letter LetterOrDigit*;

fragment
Letter : [a-zA-Z$_];

fragment
LetterOrDigit : [a-zA-Z0-9$_];


WS  : [ \t\r\n\u000C]+ -> skip;

COMMENT : '/*' .*? '*/' -> skip;

LINE_COMMENT : '//' ~[\r\n]* -> skip;


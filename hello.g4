grammar hello;

body    :   declaration* EOF    ;

declaration
    :   variabledeclaration                                                                                             # VarDeclar
    |   classdeclaration                                                                                                # ClassDeclar
    |   functiondeclaration                                                                                             # FuncDeclar
    ;

variabledeclaration :   typename (initialize ',')* initialize ';'   ;

typename
    :   easytype                                                                                                        # PrimeCase
    |   Identifier                                                                                                      # ClassCase
    |   typename '['']'                                                                                                 # ArrayCase
    ;

easytype
    :   BOOL
    |   INT
    |   VOID
    |   STRING
    ;

initialize  :   id=Identifier ('=' expression)?;

expression
    :   lhsexpression                                                                                                   # LhsExpr
    |   constexpression                                                                                                 # ConstExpr
    |   newexpression                                                                                                   # NewExpr
    |   lhs=expression op=('++'|'--')                                                                                   # PostfixUpdateExpr
    |   op=('++'|'--') expression                                                                                       # PrefixUpdateExpr
    |   <assoc=right> op=('!'|'-'|'+'|'~') rhs=expression                                                               # UnaryExpr
    |   <assoc=right> lhs=expression op='**' rhs=expression                                                             # ExpExpr
    |   lhs=expression op=('*'|'/'|'%') rhs=expression                                                                  # BinaryExpr
    |   lhs=expression op=('+'|'-') rhs=expression                                                                      # BinaryExpr
    |   lhs=expression op=('<<'|'>>') rhs=expression                                                                    # BinaryExpr
    |   lhs=expression op=('<'|'>'|'<='|'>=') rhs=expression                                                            # BinaryExpr
    |   lhs=expression op=('=='|'!=') rhs=expression                                                                    # BinaryExpr
    |   lhs=expression op='&' rhs=expression                                                                            # BinaryExpr
    |   lhs=expression op='^' rhs=expression                                                                            # BinaryExpr
    |   lhs=expression op='|' rhs=expression                                                                            # BinaryExpr
    |   lhs=expression op='&&' rhs=expression                                                                           # BinaryExpr
    |   lhs=expression op='||' rhs=expression                                                                           # BinaryExpr
    |   <assoc=right> lhs=lhsexpression '=' rhs=expression                                                              # AssignExpr
    |   con=expression '?' lhs=expression ':' rhs=expression                                                            # TriExpr
    ;

newexpression   :   NEW newtypename ('('')')?   ;

newtypename
    :   Identifier                                                                                                      # NewClass
    |   Identifier bracketwithargs+ bracketwithoutargs*                                                                 # NewClassArray
    |   easytype bracketwithargs+ bracketwithoutargs*                                                                   # NewPrimeArray
    ;

bracketwithargs :   '['expression ']'   ;
bracketwithoutargs  :   '['']'  ;

constexpression
    :   Interger                                                                                                        # Numconstexpression
    |   String                                                                                                          # Stringconstexpression
    |  ( TRUE | FALSE)                                                                                                  # Boolconstexpression
    |   NULL                                                                                                            # Nullconstexpression
    ;

lhsexpression
    :   Identifier                                                                                                      # IdentifierExpr
    |   THIS                                                                                                            # ThisExpr
    |   lhsexpression '.' Identifier                                                                                    # MemberVarExpr
    |   lhsexpression '.' '('Identifier')'                                                                              # MemberVarExpr
    |   lhsexpression '.' Identifier '(' funcarglist? ')'                                                               # MemberFuncExpr
    |   lhsexpression '[' expression ']'                                                                                # ArrayExpr
    |   Identifier '(' funcarglist? ')'                                                                                 # FuncCallExpr
    |   '(' expression ')'                                                                                              # ParaExpr
    ;

funcarglist :   (expression ',')* expression   ;

classdeclaration    :   CLASS Identifier '{' classFuncdeclar* '}' ';'  ;

classFuncdeclar
    :   variabledeclaration                                                                                             # ClassMemberDeclar
    |   functiondeclaration                                                                                             # ClassMemberFuncDeclar
    |   classConstructFunc                                                                                              # ClassConstructorDeclar
    ;

classConstructFunc  :   Identifier '(' ')' blockStatement   ;

blockStatement  : '{' statement* '}' ;

functiondeclaration :   typename Identifier '(' funcarglistDec? ')' blockStatement;

funcarglistDec  :  ( funcparam ',')* funcparam;

funcparam  :   typename Identifier ;

statement
    :   blockStatement                                                                                                  # BlockSmt
    |   variabledeclaration                                                                                             # VarDeclarSmt
    |   expression ';'                                                                                                  # ExprSmt
    |   branchStatement                                                                                                 # BranchSmt
    |   loopStatement                                                                                                   # LoopSmt
    |   CONTI ';'                                                                                                       # ContinueSmt
    |   BREAK ';'                                                                                                       # BreakSmt
    |   RET expression? ';'                                                                                             # ReturnSmt
    |   emptyStatement                                                                                                  # EmptySmt
    ;

branchStatement :   IF  '(' cond=expression ')' ifsmt=statement (ELSE elsesmt=statement)?  ;


loopStatement
    :   WHILE '(' cond=expression ')' statement                                                                         # WhileSmt
    |   FOR '(' init=variabledeclaration cond=expression?';' step=expression? ')' statement                             # DecForSmt
    |   FOR '(' init=expression?';' cond=expression?';' step=expression? ')' statement                                  # ExpForSmt
    ;
emptyStatement  :   ';' ;

LineComment: '//' ~[\r\n]* -> channel(HIDDEN);

BlockComment: '/*' .*? '*/' -> channel(HIDDEN);

Interger
    :   '0'
    |   [1-9][0-9]*
    ;

BOOL    :   'bool'      ;
INT     :   'int'       ;
VOID    :   'void'      ;
STRING  :   'string'    ;
IF      :   'if'        ;
ELSE    :   'else'      ;
NEW     :   'new'       ;
CLASS   :   'class'     ;
TRUE    :   'true'      ;
FALSE   :   'false'     ;
NULL    :   'null'      ;
THIS    :   'this'      ;
FOR     :   'for'       ;
WHILE   :   'while'     ;
BREAK   :   'break'     ;
CONTI   :   'continue'  ;
RET     :   'return'    ;
MUL     :   '*' ;
DIV     :   '/' ;
MOD     :   '%' ;
ADD     :   '+' ;
SUB     :   '-' ;
Identifier  :   [a-zA-Z][a-zA-Z_0-9]*   ;

fragment Escapecharacter
    :   'n'
    |   '\\'
    |   '"'
    ;
fragment Stringchar
    : ~["\\\n\r]
    | '\\' Escapecharacter
    ;

String  :   '"' Stringchar* '"' ;

WS  :   [ \t\n\r]+ -> channel(HIDDEN)  ;


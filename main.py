import os
import time

from antlr4 import *
from py_parser.helloLexer import helloLexer
from py_parser.helloParser import helloParser
from enum import Enum
import sys
from antlr4.error.ErrorListener import ErrorListener


def getstring(str):
    res = ""
    i = 1
    while (i < len(str) - 1):
        if str[i] != '\\':
            res = res + str[i]
        else:
            if str[i + 1] == '\\':
                res = res + '\\'
                i = i + 1
            elif str[i + 1] == 'n':
                res = res + '\n'
                i = i + 1
            elif str[i + 1] == '\"':
                res = res + '\"'
                i = i + 1
            else:
                raise Exception("Error in getstring:", str)
        i = i + 1
    return res


class MyErrorListener(ErrorListener):
    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        # print(str(line) + ":" + str(column) + ": sintax ERROR, " + str(msg))
        # print("Terminating Translation")
        raise Exception("Build Error")


class typeEnum(Enum):
    VOID = 0
    NULL = 1
    INT = 2
    BOOL = 3
    STRING = 4
    CLASS = 5


class typeclass:
    def __init__(self, t=typeEnum.VOID, name="", dim=0):
        self.type = t
        self.name = name
        self.dim = dim

    def __eq__(self, other):
        if other == None:
            return False
        return self.type == other.type and self.name == other.name and self.dim == other.dim

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(self.type, self.name, self.dim, end="|")


def gettype(node):
    if type(node).__name__ == 'PrimeCaseContext':
        return gettype(node.children[0])
    if type(node).__name__ == 'EasytypeContext':
        return gettype(node.children[0])
    if type(node).__name__ == 'ClassCaseContext':
        return gettype(node.children[0])
    if type(node).__name__ == 'ArrayCaseContext':
        dim = 0
        temp = node
        while type(temp).__name__ == 'ArrayCaseContext':
            dim += 1
            temp = temp.children[0]
        basetype = gettype(temp)
        basetype.dim = dim
        return basetype
    if type(node).__name__ == 'TerminalNodeImpl':
        if node.symbol.type == helloParser.INT:
            return typeclass(t=typeEnum.INT)
        if node.symbol.type == helloParser.BOOL:
            return typeclass(t=typeEnum.BOOL)
        if node.symbol.type == helloParser.STRING:
            return typeclass(t=typeEnum.STRING)
        if node.symbol.type == helloParser.VOID:
            return typeclass(t=typeEnum.VOID)
        if node.symbol.type == helloParser.Identifier:
            return typeclass(t=typeEnum.CLASS, name=node.symbol.text)
    raise Exception("Unknow Error in gettype")


class ASTEmptyNode:
    def __init__(self):
        pass

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__)

    def __eq__(self, other):
        return type(other).__name__ == 'ASTEmptyNode'


class ASTVariabledeclarationNode:
    def __init__(self, type=typeclass()):
        self.type = type
        self.init = []

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__, "| type:", end="")
        self.type.__debugger__(0)
        print("init:")
        for i in self.init:
            i.__debugger__(n + 1)


class ASTInitializeContextNode:
    def __init__(self, id="", expr=ASTEmptyNode()):
        self.id = id
        self.expr = expr

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__, end='|')
        print("id:", self.id, end="| = \n")
        self.expr.__debugger__(n + 1)


class ASTConstExprContextNode:
    def __init__(self, t=None, v=None):
        self.type = t
        self.value = v

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__, "| type:", end='')
        self.type.__debugger__(0)
        print("value: ", self.value)


class ASTIdentifierExprNode:
    def __init__(self, id=""):
        self.id = id

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__, "id: ", self.id)


class ASTMemberVarExprNode:
    def __init__(self, body=None, id=""):
        self.body = body
        self.id = id

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__, "id: ", self.id, "| body:")
        self.body.__debugger__(n + 1)


class ASTMemberFuncExprNode:
    def __init__(self, body=None, id="", args=[]):
        self.body = body
        self.id = id
        self.args = args

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__, "id: ", self.id, "|args:")
        for arg in self.args:
            arg.__debugger__(n + 1)
        for i in range(n):
            print('\t', end='')
        print("body: ")
        self.body.__debugger__(n + 1)


class ASTArrayExprNode:
    def __init__(self, body=None, ind=None):
        self.body = body
        self.ind = ind

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__, "ind: ")
        self.ind.__debugger__(n + 1)
        for i in range(n):
            print('\t', end='')
        print("body: ")
        self.body.__debugger__(n + 1)


class ASTFuncCallExprNode:
    def __init__(self, id="", args=[]):
        self.id = id
        self.args = args

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__, "id: ", self.id, "|args: ")
        for arg in self.args:
            arg.__debugger__(n + 1)


class ASTPrefixUpdateExprNode:
    def __init__(self, op="", body=None):
        self.body = body
        self.op = op

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__, self.op, "body: ")
        self.body.__debugger__(n + 1)


class ASTPostfixUpdateExprNode:
    def __init__(self, op="", body=None):
        self.op = op
        self.body = body

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__, "body", self.op, ": ")
        self.body.__debugger__(n + 1)


class ASTNewArrayContextNode:
    def __init__(self, t=typeEnum.VOID, dims=[]):
        self.type = t
        self.dims = dims

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__, "type: ", end="")
        self.type.__debugger__(0)
        print("dims: ")
        for i in self.dims:
            i.__debugger__(n + 1)


class ASTNewClassNode:
    def __init__(self, id=""):
        self.id = id

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__, "id: ", self.id)


class ASTUnaryExprNode:
    def __init__(self, op="", body=None):
        self.op = op
        self.body = body

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__, self.op, "body: ")
        self.body.__debugger__(n + 1)


class ASTBinaryExprNode:
    def __init__(self, op="", lhs=ASTEmptyNode(), rhs=ASTEmptyNode()):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__, "lhs: ")
        self.lhs.__debugger__(n + 1)
        for i in range(n):
            print('\t', end='')
        print(self.op, "rhs: ")
        self.rhs.__debugger__(n + 1)


class ASTAssignExprNode:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__, "lhs: ")
        self.lhs.__debugger__(n + 1)
        for i in range(n):
            print('\t', end='')
        print("Assign rhs: ")
        self.rhs.__debugger__(n + 1)


class ASTTriExprNode:
    def __init__(self, condition=None, lhs=None, rhs=None):
        self.condition = condition
        self.lhs = lhs
        self.rhs = rhs

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__, "condition: ")
        self.condition.__debugger__(n + 1)
        for i in range(n):
            print('\t', end='')
        print("lhs: ")
        self.lhs.__debugger__(n + 1)
        for i in range(n):
            print('\t', end='')
        print("rhs: ")
        self.rhs.__debugger__(n + 1)


class ASTBlockSmtNode:
    def __init__(self):
        self.Smt = []

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print("blockSmt:")
        for smt in self.Smt:
            smt.__debugger__(n + 1)


class ASTFunctiondeclarationContextNode:
    def __init__(self, t=typeEnum.VOID, id="", arglist=[], blockSmt=ASTBlockSmtNode()):
        self.retType = t
        self.id = id
        self.arglist = arglist
        self.BlockSmt = blockSmt

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__, "id: ", self.id, "|return type: ", end="")
        self.retType.__debugger__(0)
        print("arglist: ")
        for arg in self.arglist:
            arg.__debugger__(n + 1)
        for i in range(n):
            print('\t', end='')
        print("Statement: ")
        self.BlockSmt.__debugger__(n + 1)


class ASTFuncparamContextNode:
    def __init__(self, t=typeEnum.VOID, id=""):
        self.type = t
        self.id = id

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__, "type: ", end="")
        self.type.__debugger__(0)
        print("id: ", self.id)


class ASTBranchStatementNode:
    def __init__(self, condition=ASTEmptyNode(), ifSmt=ASTEmptyNode(), elseSmt=ASTEmptyNode()):
        self.condition = condition
        self.ifSmt = ifSmt
        self.elseSmt = elseSmt

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__)
        for i in range(n + 1):
            print('\t', end='')
        print("condition:")
        self.condition.__debugger__(n + 2)
        for i in range(n + 1):
            print('\t', end='')
        print("ifSmt:")
        self.ifSmt.__debugger__(n + 2)
        for i in range(n + 1):
            print('\t', end='')
        print("elseSmt:")
        self.elseSmt.__debugger__(n + 2)


class ASTLoopForNode:
    def __init__(self, initExpr=ASTEmptyNode(), endCondition=ASTEmptyNode(), step=ASTEmptyNode(), Smt=ASTEmptyNode()):
        self.initExpr = initExpr
        self.endCondition = endCondition
        self.step = step
        self.Smt = Smt

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__)
        for i in range(n + 1):
            print('\t', end='')
        print("initExpr:")
        self.initExpr.__debugger__(n + 2)
        for i in range(n + 1):
            print('\t', end='')
        print("endCondition:")
        self.endCondition.__debugger__(n + 2)
        for i in range(n + 1):
            print('\t', end='')
        print("step:")
        self.step.__debugger__(n + 2)
        for i in range(n + 1):
            print('\t', end='')
        print("Smt:")
        self.Smt.__debugger__(n + 2)


class ASTLoopWhileNode:
    def __init__(self, Condition=ASTEmptyNode(), Smt=ASTEmptyNode()):
        self.Condition = Condition
        self.Smt = Smt

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__)
        for i in range(n + 1):
            print('\t', end='')
        print("Condition:")
        self.Condition.__debugger__(n + 2)
        for i in range(n + 1):
            print('\t', end='')
        print("Smt:")
        self.Smt.__debugger__(n + 2)


class ASTControlNode:
    def __init__(self, cmd="", returnExpr=ASTEmptyNode()):
        self.cmd = cmd
        self.returnExpr = returnExpr

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__, "cmd: ", self.cmd)
        for i in range(n + 1):
            print('\t', end='')
        print("returnExpr:")
        self.returnExpr.__debugger__(n + 2)


class ASTClassdeclarationContextNode:
    def __init__(self, id="", ClassMember=[], FunctionMember=[], ConstructFunc=ASTEmptyNode()):
        self.id = id
        self.ClassMember = ClassMember
        self.FunctionMember = FunctionMember
        self.ConstructFunc = ConstructFunc

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__, "id: ", self.id)
        for i in range(n + 1):
            print('\t', end='')
        print("ClassMember:")
        for member in self.ClassMember:
            member.__debugger__(n + 2)
        for i in range(n + 1):
            print('\t', end='')
        print("FunctionMem:")
        for member in self.FunctionMember:
            member.__debugger__(n + 2)
        for i in range(n + 1):
            print('\t', end='')
        print("ConstructFunc:")
        self.ConstructFunc.__debugger__(n + 2)


class ASTBodyRootNode():
    def __init__(self):
        self.children = []

    def __debugger__(self, n):
        for i in range(n):
            print('\t', end='')
        print(type(self).__name__)
        for i in range(n + 1):
            print('\t', end='')
        print("Children:")
        for member in self.children:
            member.__debugger__(n + 2)


class ScopeEnum(Enum):
    Global = 0
    Loop = 2
    Class = 3
    Func = 4
    Block = 5


class Scope:
    def __init__(self, type, name=""):
        self.VarsBank = {}
        self.type = type
        self.name = name


class ClassScope:
    def __init__(self, id="", ClassMember={}, FunctionMember={}):
        self.ClassMember = ClassMember
        self.FunctionMember = FunctionMember
        self.id = id


class ASTBuilder:
    def __init__(self):
        self.FuncBank = {}
        self.ClassBank = {}
        self.Scopes = [Scope(type=ScopeEnum.Global)]
        # 数组的内建方法
        self.ClassBank['int'] = ClassScope(id='int', FunctionMember={
            'size': ASTFunctiondeclarationContextNode(t=typeclass(t=typeEnum.INT), id='size', arglist=[])})
        # 字符串的内建方法
        self.ClassBank['string'] = ClassScope(id='string', FunctionMember={
            'length': ASTFunctiondeclarationContextNode(t=typeclass(t=typeEnum.INT), id='length'),
            'substring': ASTFunctiondeclarationContextNode(t=typeclass(t=typeEnum.STRING), id='substring', arglist=[
                ASTFuncparamContextNode(t=typeclass(t=typeEnum.INT)),
                ASTFuncparamContextNode(t=typeclass(t=typeEnum.INT))]),
            'parseInt': ASTFunctiondeclarationContextNode(t=typeclass(t=typeEnum.INT), id='parseInt'),
            'ord': ASTFunctiondeclarationContextNode(t=typeclass(t=typeEnum.INT), id='ord', arglist=[
                ASTFuncparamContextNode(t=typeclass(t=typeEnum.INT))])})

        # 内建函数
        self.FuncBank['print'] = ASTFunctiondeclarationContextNode(t=typeclass(t=typeEnum.VOID), id='print', arglist=[
            ASTFuncparamContextNode(t=typeclass(t=typeEnum.STRING))])
        self.FuncBank['println'] = ASTFunctiondeclarationContextNode(t=typeclass(t=typeEnum.VOID), id='println', arglist=[
            ASTFuncparamContextNode(t=typeclass(t=typeEnum.STRING))])
        self.FuncBank['printInt'] = ASTFunctiondeclarationContextNode(t=typeclass(t=typeEnum.VOID), id='printInt', arglist=[
            ASTFuncparamContextNode(t=typeclass(t=typeEnum.INT))])
        self.FuncBank['printlnInt'] = ASTFunctiondeclarationContextNode(t=typeclass(t=typeEnum.VOID), id='printlnInt', arglist=[
            ASTFuncparamContextNode(t=typeclass(t=typeEnum.INT))])
        self.FuncBank['getString'] = ASTFunctiondeclarationContextNode(t=typeclass(t=typeEnum.STRING), id='getString')
        self.FuncBank['getInt'] = ASTFunctiondeclarationContextNode(t=typeclass(t=typeEnum.INT), id='getInt')
        self.FuncBank['toString'] = ASTFunctiondeclarationContextNode(t=typeclass(t=typeEnum.STRING), id='toString', arglist=[
            ASTFuncparamContextNode(t=typeclass(t=typeEnum.INT))])

    def build(self, node):
        if not isinstance(node, ParserRuleContext):
            raise Exception(f"{node} must be a node, not a {type(node)}")
        name = "build" + type(node).__name__
        return self.__getattribute__(name)(node)

    def buildBodyContext(self, node):
        res = ASTBodyRootNode()
        for i in range(0, len(node.children) - 1, 1):
            res.children.append(self.build(node.children[i]))
        return res

    def buildClassDeclarContext(self, node):
        return self.buildClassdeclarationContext(node.children[0])

    def buildVarDeclarContext(self, node):
        return self.buildVariabledeclarationContext(node.children[0])

    def buildFuncDeclarContext(self, node):
        return self.buildFunctiondeclarationContext(node.children[0])

    def buildVariabledeclarationContext(self, node):
        res = ASTVariabledeclarationNode(type=gettype(node.children[0]))
        for i in range(1, len(node.children), 2):
            self.buildInitializeContext(res, node.children[i])
        return res

    def buildConstExprContext(self, node):
        if type(node.children[0]).__name__ == 'NumconstexpressionContext':
            return ASTConstExprContextNode(typeclass(typeEnum.INT), int(eval(node.children[0].children[0].symbol.text)))
        if type(node.children[0]).__name__ == 'BoolconstexpressionContext':
            return ASTConstExprContextNode(typeclass(typeEnum.BOOL), node.children[0].children[0].symbol.text == "true")
        if type(node.children[0]).__name__ == 'StringconstexpressionContext':
            return ASTConstExprContextNode(typeclass(typeEnum.STRING),
                                           getstring(node.children[0].children[0].symbol.text))
        if type(node.children[0]).__name__ == 'NullconstexpressionContext':
            return ASTConstExprContextNode(typeclass(typeEnum.NULL), None)
        raise Exception("Unknow Error in buildConstExprContext")

    def buildInitializeContext(self, target, node):
        if len(node.children) == 3:
            res = ASTInitializeContextNode(id=node.children[0].symbol.text, expr=self.build(node.children[2]))
        else:
            res = ASTInitializeContextNode(id=node.children[0].symbol.text, expr=ASTEmptyNode())
        target.init.append(res)

    def buildLhsExprContext(self, node):
        return self.build(node.children[0])

    def buildIdentifierExprContext(self, node):
        return ASTIdentifierExprNode(node.children[0].symbol.text)

    def buildMemberVarExprContext(self, node):
        return ASTMemberVarExprNode(self.build(node.children[0]), node.children[2].symbol.text)

    def buildThisExprContext(self, node):
        return ASTIdentifierExprNode(node.children[0].symbol.text)

    def buildMemberFuncExprContext(self, node):
        res = ASTMemberFuncExprNode(body=self.build(node.children[0]), id=node.children[2].symbol.text, args=[])
        if len(node.children) == 6:
            res.args = self.makefuncargs(node.children[4])
        return res

    def buildArrayExprContext(self, node):
        return ASTArrayExprNode(self.build(node.children[0]), self.build(node.children[2]))

    def buildFuncCallExprContext(self, node):
        res = ASTFuncCallExprNode(node.children[0].symbol.text)
        if len(node.children) == 4:
            res.args = self.makefuncargs(node.children[2])
        return res

    def buildPrefixUpdateExprContext(self, node):
        return ASTPrefixUpdateExprNode(op=node.op.text, body=self.build(node.children[1]))

    def buildNewExprContext(self, node):
        return self.build(node.children[0].children[1])

    def buildNewPrimeArrayContext(self, node):
        res = ASTNewArrayContextNode(t=gettype(node.children[0]), dims=[])
        for i in range(1, len(node.children)):
            res.dims.append(self.bracket(node.children[i]))
        return res

    def buildNewClassArrayContext(self, node):
        res = ASTNewArrayContextNode(t=gettype(node.children[0]), dims=[])
        for i in range(1, len(node.children)):
            res.dims.append(self.bracket(node.children[i]))
        return res

    def buildNewClassContext(self, node):
        return ASTNewClassNode(id=node.children[0].symbol.text)

    def buildParaExprContext(self, node):
        return self.build(node.children[1])

    def buildPostfixUpdateExprContext(self, node):
        return ASTPostfixUpdateExprNode(op=node.op.text, body=self.build(node.children[0]))

    def buildUnaryExprContext(self, node):
        return ASTUnaryExprNode(op=node.op.text, body=self.build(node.children[1]))

    def buildExpExprContext(self, node):
        return ASTBinaryExprNode(op=node.op.text, lhs=self.build(node.lhs), rhs=self.build(node.rhs))

    def buildBinaryExprContext(self, node):
        return ASTBinaryExprNode(op=node.op.text, lhs=self.build(node.lhs), rhs=self.build(node.rhs))

    def buildAssignExprContext(self, node):
        return ASTAssignExprNode(lhs=self.build(node.children[0]), rhs=self.build(node.children[2]))

    def buildTriExprContext(self, node):
        return ASTTriExprNode(condition=self.build(node.children[0]), lhs=self.build(node.children[2]),
                              rhs=self.build(node.children[4]))

    def buildFunctiondeclarationContext(self, node):
        res = ASTFunctiondeclarationContextNode(t=gettype(node.children[0]), id=node.children[1].symbol.text, blockSmt=ASTBlockSmtNode())
        if len(node.children) == 6:
            res.arglist = self.makefuncargs(node.children[3])
        self.buildblockSmt(res.BlockSmt, node.children[-1])
        return res

    def buildFuncparamContext(self, node):
        return ASTFuncparamContextNode(t=gettype(node.children[0]), id=node.children[1].symbol.text)

    def buildblockSmt(self, target, node):
        for i in range(1, len(node.children) - 1):
            target.Smt.append(self.build(node.children[i]))

    def buildVarDeclarSmtContext(self, node):
        return self.buildVariabledeclarationContext(node.children[0])

    def buildBlockSmtContext(self, node):
        res = ASTBlockSmtNode()
        self.buildblockSmt(res, node.children[0])
        return res

    def buildExprSmtContext(self, node):
        return self.build(node.children[0])

    def buildEmptySmtContext(self, node):
        return ASTEmptyNode()

    def buildBranchSmtContext(self, node):
        return self.buildBranchStatementContext(node.children[0])

    def buildBranchStatementContext(self, node):
        res = ASTBranchStatementNode()
        if node.cond != None:
            res.condition = self.build(node.cond)
        if node.ifsmt != None:
            res.ifSmt = self.build(node.ifsmt)
        if node.elsesmt != None:
            res.elseSmt = self.build(node.elsesmt)
        return res

    def buildLoopSmtContext(self, node):
        return self.build(node.children[0])

    def buildDecForSmtContext(self, node):
        res = ASTLoopForNode()
        if node.init != None:
            res.initExpr = self.build(node.init)
        if node.cond != None:
            res.endCondition = self.build(node.cond)
        if node.step != None:
            res.step = self.build(node.step)
        res.Smt = self.build(node.children[-1])
        return res

    def buildExpForSmtContext(self, node):
        res = ASTLoopForNode()
        if node.init != None:
            res.initExpr = self.build(node.init)
        if node.cond != None:
            res.endCondition = self.build(node.cond)
        if node.step != None:
            res.step = self.build(node.step)
        res.Smt = self.build(node.children[-1])
        return res

    def buildWhileSmtContext(self, node):
        return ASTLoopWhileNode(Condition=self.build(node.cond), Smt=self.build(node.children[-1]))

    def buildBreakSmtContext(self, node):
        return ASTControlNode(cmd="Break")

    def buildContinueSmtContext(self, node):
        return ASTControlNode(cmd="Continue")

    def buildReturnSmtContext(self, node):
        res = ASTControlNode(cmd="Return")
        if len(node.children) == 3:
            res.returnExpr = self.build(node.children[1])
        return res

    def buildClassdeclarationContext(self, node):
        res = ASTClassdeclarationContextNode(id=node.children[1].symbol.text, ClassMember=[], FunctionMember=[])
        for i in range(3, len(node.children) - 2, 1):
            self.buildclassFuncdeclar(res, node.children[i])
        return res

    def buildclassFuncdeclar(self, target, node):
        if type(node).__name__ == 'ClassMemberDeclarContext':
            target.ClassMember.append(self.build(node.children[0]))
        elif type(node).__name__ == 'ClassMemberFuncDeclarContext':
            target.FunctionMember.append(self.build(node.children[0]))
        elif type(node).__name__ == 'ClassConstructorDeclarContext':
            if target.ConstructFunc == ASTEmptyNode():
                target.ConstructFunc = self.build(node.children[0])
            else:
                raise Exception(f"Class {target.id} can only have unique ClassConstructorDeclarContext")
        else:
            raise Exception(f"Class {target.id} cannot accept node as {type(node).__name__}")

    def buildClassConstructFuncContext(self, node):
        res = ASTFunctiondeclarationContextNode(t=typeclass(t=typeEnum.VOID), id=node.children[0].symbol.text, blockSmt=ASTBlockSmtNode())
        self.buildblockSmt(res.BlockSmt, node.children[-1])
        return res

    def bracket(self, node):
        if type(node).__name__ == 'BracketwithargsContext':
            return self.build(node.children[1])
        if type(node).__name__ == 'BracketwithoutargsContext':
            return ASTEmptyNode()
        raise Exception(f"{node} must be a bracketContext, not a {type(node).__name__}")

    def makefuncargs(self, node):
        if type(node).__name__ != 'FuncarglistContext' and type(node).__name__ != 'FuncarglistDecContext':
            raise Exception(f"{node} must be a FuncarglistContext|FuncarglistDecContext, not a {type(node)}")
        res = []
        for i in range(0, len(node.children), 2):
            res.append(self.build(node.children[i]))
        return res

    def check(self, node):
        name = "check" + type(node).__name__
        return self.__getattribute__(name)(node)

    def checkrepeat(self, id):
        for i in range(len(self.Scopes) - 1, -1, -1):
            if id in self.Scopes[i].VarsBank:
                return i
        return -1

    def typeget(self, node):
        name = "type" + type(node).__name__
        return self.__getattribute__(name)(node)

    def checktype(self, type, node):
        nodestype, _, check = self.typeget(node)
        if check:
            if type == nodestype:
                return True
            elif type.dim > 0:
                return nodestype == typeclass(t=typeEnum.NULL)
            elif type.type == typeEnum.CLASS:
                return nodestype == typeclass(t=typeEnum.NULL)
        return False

    def checkASTBodyRootNode(self, node):
        for child in node.children:
            if type(child).__name__ == 'ASTVariabledeclarationNode':
                continue
                # for ids in child.init:
                #     typecheck = self.checktype(child.type, ids.expr)
                #     repeatcheck = self.checkrepeat(ids.id)
                #     if typecheck and repeatcheck != 0:
                #         self.Scopes[0].VarsBank[ids.id] = child.type
                #     else:
                #         return False
            elif type(child).__name__ == 'ASTFunctiondeclarationContextNode':
                if (self.checkrepeat(child.id) == -1) and (child.id not in self.FuncBank) and (
                        child.id not in self.ClassBank):
                    self.FuncBank[child.id] = child
                else:
                    return False
            elif type(child).__name__ == 'ASTClassdeclarationContextNode':
                if (child.id not in self.FuncBank) and (child.id not in self.ClassBank):
                    self.ClassBank[child.id] = ClassScope(id=child.id, FunctionMember={}, ClassMember={})
                    for classmember in child.ClassMember:
                        for ids in classmember.init:
                            if ids.id not in self.ClassBank[child.id].ClassMember:
                                self.ClassBank[child.id].ClassMember[ids.id] = ASTFuncparamContextNode(t=classmember.type, id=ids.id)
                            else:
                                return False
                    for funcmember in child.FunctionMember:
                        if funcmember.id not in self.ClassBank[child.id].FunctionMember:
                            self.ClassBank[child.id].FunctionMember[funcmember.id] = ASTFunctiondeclarationContextNode(t=funcmember.retType,
                                                                                                                       arglist=funcmember.arglist,
                                                                                                                       id=funcmember.id)
                        else:
                            return False

                else:
                    return False
        if ('main' not in self.FuncBank) or (self.FuncBank['main'].retType != typeclass(t=typeEnum.INT)) or (
                len(self.FuncBank['main'].arglist) != 0):
            return False
        for child in node.children:
            checkchild = self.check(child)
            if checkchild == False:
                # child.__debugger__(0)
                return False
        return True

    def typevarscheck(self, type):
        if type.type in [typeEnum.INT, typeEnum.BOOL, typeEnum.STRING]:
            return True
        elif (type.type == typeEnum.CLASS) and (type.name in self.ClassBank):
            return True
        else:
            return False

    def checkASTVariabledeclarationNode(self, node):
        for ids in node.init:
            if ids.expr == ASTEmptyNode():
                if self.typevarscheck(node.type) and (self.checkrepeat(ids.id) != len(self.Scopes) - 1) and (ids.id not in self.FuncBank):
                    self.Scopes[-1].VarsBank[ids.id] = node.type
                else:
                    return False
            elif self.checktype(node.type, ids.expr) and (self.checkrepeat(ids.id) != len(self.Scopes) - 1) and self.typevarscheck(
                    node.type) and (ids.id not in self.FuncBank):
                self.Scopes[-1].VarsBank[ids.id] = node.type
            else:
                return False
        return True

    def checkfuncASTVariabledeclarationNode(self, funcnode, smt):
        return None, self.checkASTVariabledeclarationNode(smt)

    def typeASTConstExprContextNode(self, node):
        return node.type, False, True

    def checkfuncASTConstExprContextNode(self, funcnode, smt):
        _, _, check = self.typeget(smt)
        return None, check

    def typeASTIdentifierExprNode(self, node):
        for i in range(len(self.Scopes) - 1, -1, -1):
            if node.id in self.Scopes[i].VarsBank:
                if node.id == 'this':
                    return self.Scopes[i].VarsBank[node.id], False, True
                else:
                    return self.Scopes[i].VarsBank[node.id], True, True
        return None, False, False

    def checkfuncASTIdentifierExprNode(self, funcnode, smt):
        _, _, check = self.typeget(smt)
        return None, check

    def typeASTBinaryExprNode(self, node):
        type1, _, check1 = self.typeget(node.lhs)
        type2, _, check2 = self.typeget(node.rhs)
        if check1 and check2:
            if node.op in ['*', '/', '%', '-', '<<', '>>', '&', '^', '|']:  # 两边都是Int
                if type1 == typeclass(t=typeEnum.INT) and type2 == typeclass(t=typeEnum.INT):
                    return typeclass(t=typeEnum.INT), False, True
                else:
                    return None, False, False
            elif node.op in ['&&', '||']:  # 两边都是Bool
                if type1 == typeclass(t=typeEnum.BOOL) and type2 == typeclass(t=typeEnum.BOOL):
                    return typeclass(t=typeEnum.BOOL), False, True
                else:
                    return None, False, False
            elif node.op == '+':
                if type1 == type2:
                    if type1 == typeclass(t=typeEnum.INT):
                        return typeclass(t=typeEnum.INT), False, True
                    elif type1 == typeclass(t=typeEnum.STRING):
                        return typeclass(t=typeEnum.STRING), False, True
                    else:
                        return None, False, False
                else:
                    return None, False, False
            elif node.op in ['<', '>', '<=', '>=']:
                if type1 == type2:
                    if type1 == typeclass(t=typeEnum.INT):
                        return typeclass(t=typeEnum.BOOL), False, True
                    elif type1 == typeclass(t=typeEnum.STRING):
                        return typeclass(t=typeEnum.BOOL), False, True
                    else:
                        return None, False, False
                else:
                    return None, False, False
            elif node.op in ['==', '!=']:
                if type1 == type2:
                    if type1 == typeclass(t=typeEnum.INT):
                        return typeclass(t=typeEnum.BOOL), False, True
                    elif type1 == typeclass(t=typeEnum.STRING):
                        return typeclass(t=typeEnum.BOOL), False, True
                    elif type1 == typeclass(t=typeEnum.BOOL):
                        return typeclass(t=typeEnum.BOOL), False, True
                    elif type1 == typeclass(t=typeEnum.CLASS):
                        return typeclass(t=typeEnum.BOOL), False, True
                    elif type1 == typeclass(t=typeEnum.NULL):
                        return typeclass(t=typeEnum.BOOL), False, True
                    else:
                        return None, False, False
                else:
                    if type1.dim > 0 and type2 == typeclass(t=typeEnum.NULL):
                        return typeclass(t=typeEnum.BOOL), False, True
                    elif type2.dim > 0 and type1 == typeclass(t=typeEnum.NULL):
                        return typeclass(t=typeEnum.BOOL), False, True
                    elif type1.type == typeEnum.CLASS and type2 == typeclass(t=typeEnum.NULL):
                        return typeclass(t=typeEnum.BOOL), False, True
                    elif type2.type == typeEnum.CLASS and type1 == typeclass(t=typeEnum.NULL):
                        return typeclass(t=typeEnum.BOOL), False, True
                    else:
                        return None, False, False
        else:
            return None, False, False

    def checkfuncASTBinaryExprNode(self, funcnode, smt):
        _, _, check = self.typeget(smt)
        return None, check

    def typeASTMemberVarExprNode(self, node):
        bodytype, _, check = self.typeget(node.body)
        if check:
            if bodytype == typeclass(t=typeEnum.CLASS, name=bodytype.name):
                if bodytype.name in self.ClassBank:
                    if node.id in self.ClassBank[bodytype.name].ClassMember:
                        return self.ClassBank[bodytype.name].ClassMember[node.id].type, True, True
        return None, False, False

    def checkfuncASTMemberVarExprNode(self, funcnode, smt):
        _, _, check = self.typeget(smt)
        return None, check

    def typeASTMemberFuncExprNode(self, node):
        bodytype, _, check = self.typeget(node.body)
        if check:
            if bodytype.dim > 0:
                if node.id == "size" and len(node.args) == 0:
                    return typeclass(t=typeEnum.INT), False, True
                else:
                    return None, False, False
            elif bodytype == typeclass(t=typeEnum.STRING):
                if node.id in self.ClassBank['string'].FunctionMember:
                    if len(node.args) != len(self.ClassBank['string'].FunctionMember[node.id].arglist):
                        return None, False, False
                    for i in range(len(self.ClassBank['string'].FunctionMember[node.id].arglist)):
                        argtype, _, argcheck = self.typeget(node.args[i])
                        if argcheck and argtype == self.ClassBank['string'].FunctionMember[node.id].arglist[i].type:
                            continue
                        else:
                            return None, False, False
                    return self.ClassBank['string'].FunctionMember[node.id].retType, False, True
                else:
                    return None, False, False
            elif bodytype == typeclass(t=typeEnum.CLASS, name=bodytype.name):
                if node.id in self.ClassBank[bodytype.name].FunctionMember:
                    if len(node.args) != len(self.ClassBank[bodytype.name].FunctionMember[node.id].arglist):
                        return None, False, False
                    for i in range(len(self.ClassBank[bodytype.name].FunctionMember[node.id].arglist)):
                        argtype, _, argcheck = self.typeget(node.args[i])
                        if argcheck and argtype == self.ClassBank[bodytype.name].FunctionMember[node.id].arglist[i].type:
                            continue
                        else:
                            return None, False, False
                    return self.ClassBank[bodytype.name].FunctionMember[node.id].retType, False, True
                else:
                    return None, False, False
        return None, False, False

    def checkfuncASTMemberFuncExprNode(self, funcnode, smt):
        _, _, check = self.typeget(smt)
        return None, check

    def typeASTUnaryExprNode(self, node):
        bodytype, _, check = self.typeget(node.body)
        if check:
            if node.op == '!':
                return typeclass(t=typeEnum.BOOL), False, (bodytype == typeclass(t=typeEnum.BOOL))
            else:
                return typeclass(t=typeEnum.INT), False, (bodytype == typeclass(t=typeEnum.INT))
        return None, False, False

    def checkfuncASTUnaryExprNode(self, funcnode, smt):
        _, _, check = self.typeget(smt)
        return None, check

    def typeASTArrayExprNode(self, node):
        bodytype, _, check = self.typeget(node.body)
        if check:
            indtype, _, indcheck = self.typeget(node.ind)
            if indcheck and indtype == typeclass(t=typeEnum.INT):
                return typeclass(t=bodytype.type, name=bodytype.name, dim=bodytype.dim - 1), True, bodytype.dim > 0
        return None, False, False

    def checkfuncASTArrayExprNode(self, funcnode, smt):
        _, _, check = self.typeget(smt)
        return None, check

    def typeASTFuncCallExprNode(self, node):
        for i in range(len(self.Scopes) - 1, -1, -1):
            if self.Scopes[i].type == ScopeEnum.Class:
                if node.id in self.ClassBank[self.Scopes[i].name].FunctionMember:
                    if len(node.args) == len(self.ClassBank[self.Scopes[i].name].FunctionMember[node.id].arglist):
                        temp = True
                        for j in range(len(node.args)):
                            if self.checktype(self.ClassBank[self.Scopes[i].name].FunctionMember[node.id].arglist[j].type, node.args[j]):
                                continue
                            else:
                                temp = False
                                break
                        if temp:
                            return self.ClassBank[self.Scopes[i].name].FunctionMember[node.id].retType, False, True

        if node.id in self.FuncBank:
            temp = True
            if len(node.args) == len(self.FuncBank[node.id].arglist):
                for i in range(len(node.args)):
                    if self.checktype(self.FuncBank[node.id].arglist[i].type, node.args[i]):
                        continue
                    else:
                        temp = False
                        break
                if temp:
                    return self.FuncBank[node.id].retType, False, True

        return None, False, False

    def checkfuncASTFuncCallExprNode(self, funcnode, smt):
        _, _, check = self.typeget(smt)
        return None, check

    def typeASTPrefixUpdateExprNode(self, node):
        bodytype, lvalue, check = self.typeget(node.body)
        if check and lvalue:
            return typeclass(t=typeEnum.INT), True, bodytype == typeclass(t=typeEnum.INT)
        return None, False, False

    def checkfuncASTPrefixUpdateExprNode(self, funcnode, smt):
        _, _, check = self.typeget(smt)
        return None, check

    def typeASTPostfixUpdateExprNode(self, node):
        bodytype, lvalue, check = self.typeget(node.body)
        if check and lvalue:
            return typeclass(t=typeEnum.INT), False, bodytype == typeclass(t=typeEnum.INT)
        return None, False, False

    def checkfuncASTPostfixUpdateExprNode(self, funcnode, smt):
        _, _, check = self.typeget(smt)
        return None, check

    def typeASTNewClassNode(self, node):
        if node.id in self.ClassBank:
            return typeclass(t=typeEnum.CLASS, name=node.id), True, True
        return None, False, False

    def checkfuncASTNewClassNode(self, funcnode, smt):
        _, _, check = self.typeget(smt)
        return None, check

    def typeASTNewArrayContextNode(self, node):
        for dim in node.dims:
            if not dim == ASTEmptyNode():
                dimtype, _, check = self.typeget(dim)
                if check and (dimtype == typeclass(t=typeEnum.INT)):
                    continue
                else:
                    return None, False, False
        return typeclass(t=node.type.type, name=node.type.name, dim=len(node.dims)), True, True

    def checkfuncASTNewArrayContextNode(self, funcnode, smt):
        _, _, check = self.typeget(smt)
        return None, check

    def typeASTAssignExprNode(self, node):
        lhstype, lvalue, lhscheck = self.typeget(node.lhs)
        rhstype, _, rhscheck = self.typeget(node.rhs)
        if lhscheck and rhscheck and lvalue:
            if lhstype == rhstype:
                return lhstype, False, True
            elif lhstype.dim > 0 and rhstype == typeclass(t=typeEnum.NULL):
                return lhstype, False, True
            elif lhstype.type == typeEnum.CLASS and rhstype == typeclass(t=typeEnum.NULL):
                return lhstype, False, True
        return None, False, False

    def checkfuncASTAssignExprNode(self, funcnode, smt):
        _, _, check = self.typeget(smt)
        return None, check

    def typeASTTriExprNode(self, node):
        conditiontype, _, conditioncheck = self.typeget(node.condition)
        if conditioncheck and (conditiontype == typeclass(t=typeEnum.BOOL)):
            lhstype, _, lhscheck = self.typeget(node.lhs)
            rhstype, _, rhscheck = self.typeget(node.rhs)
            if lhscheck and rhscheck and (lhstype == rhstype):
                return lhstype, False, True
        return None, False, False

    def checkfuncASTTriExprNode(self, funcnode, smt):
        _, _, check = self.typeget(smt)
        return None, check

    def checkASTClassdeclarationContextNode(self, node):
        self.Scopes.append(Scope(type=ScopeEnum.Class, name=node.id))
        self.Scopes[-1].VarsBank['this'] = typeclass(t=typeEnum.CLASS, name=node.id)
        for id in self.ClassBank[node.id].ClassMember:
            check = self.typevarscheck(self.ClassBank[node.id].ClassMember[id].type)
            if not check:
                return False
            self.Scopes[-1].VarsBank[id] = self.ClassBank[node.id].ClassMember[id].type
        if not node.ConstructFunc == ASTEmptyNode():
            check = self.checkClassConstructFunc(node, node.ConstructFunc)
            if not check:
                return False
        for funcnode in node.FunctionMember:
            check = self.checkclassFuncASTFunctiondeclarationContextNode(funcnode)
            if not check:
                return False
        self.Scopes.pop()
        return True

    def checkClassConstructFunc(self, classnode, funcnode):
        if funcnode.id != classnode.id:
            return False
        self.Scopes.append(Scope(type=ScopeEnum.Func))
        for smt in funcnode.BlockSmt.Smt:
            retType, check = self.checkFuncSmt(funcnode, smt)
            if check:
                if retType != None:
                    return False
            else:
                return False
        self.Scopes.pop()
        return True

    def checkFuncSmt(self, funcnode, smt):
        name = 'checkfunc' + type(smt).__name__
        return self.__getattribute__(name)(funcnode, smt)

    def checkfuncASTBlockSmtNode(self, funcnode, smt):
        self.Scopes.append(Scope(type=ScopeEnum.Block))
        retType = None
        for subsmt in smt.Smt:
            subret, check = self.checkFuncSmt(funcnode, subsmt)
            if check:
                if subret != None:
                    if not subret == funcnode.retType:
                        return None, False
                    else:
                        retType = subret
            else:
                return None, False
        self.Scopes.pop()
        return retType, True

    def checkfuncASTEmptyNode(self, funcnode, smt):
        return None, True

    def checkfuncASTBranchStatementNode(self, funcnode, smt):
        conditiontype, _, conditioncheck = self.typeget(smt.condition)
        if conditioncheck and (conditiontype == typeclass(t=typeEnum.BOOL)):
            retType = None
            self.Scopes.append(Scope(type=ScopeEnum.Block))
            ifSmtRet, ifSmtCheck = self.checkFuncSmt(funcnode, smt.ifSmt)
            self.Scopes.pop()
            if not ifSmtCheck:
                return None, False
            if ifSmtRet != None:
                if ifSmtRet == typeclass(typeEnum.NULL):
                    if funcnode.retType.dim > 0:
                        retType = ifSmtRet
                    elif funcnode.retType.type == typeEnum.CLASS:
                        retType = ifSmtRet
                    else:
                        return None, False
                elif ifSmtRet != funcnode.retType:
                    return None, False
                else:
                    retType = ifSmtRet
            self.Scopes.append(Scope(type=ScopeEnum.Block))
            elseSmtRet, elseSmtCheck = self.checkFuncSmt(funcnode, smt.elseSmt)
            self.Scopes.pop()
            if not elseSmtCheck:
                return None, False
            if elseSmtRet != None:
                if elseSmtRet == typeclass(typeEnum.NULL):
                    if funcnode.retType.dim > 0:
                        retType = elseSmtRet
                    elif funcnode.retType.type == typeEnum.CLASS:
                        retType = elseSmtRet
                    else:
                        return None, False
                elif elseSmtRet != funcnode.retType:
                    return None, False
                else:
                    retType = elseSmtRet
            return retType, True

        return None, False

    def checkfuncASTControlNode(self, funcnode, smt):
        if smt.cmd == 'Return':
            if smt.returnExpr == ASTEmptyNode():
                return None, True
            else:
                retType, _, check = self.typeget(smt.returnExpr)
                return retType, check
        else:
            for i in range(len(self.Scopes) - 1, -1, -1):
                if self.Scopes[i].type == ScopeEnum.Loop:
                    return None, True
            return None, False

    def checkfuncASTLoopForNode(self, funcnode, smt):
        self.Scopes.append(Scope(type=ScopeEnum.Loop))
        if smt.initExpr != ASTEmptyNode():
            if not self.checkFuncSmt(funcnode, smt.initExpr):
                return None, False
        if smt.endCondition != ASTEmptyNode():
            conditiontype, _, check = self.typeget(smt.endCondition)
            if (not check) or (conditiontype != typeclass(t=typeEnum.BOOL)):
                return None, False
        if smt.step != ASTEmptyNode():
            _, _, check = self.typeget(smt.step)
            if not check:
                return None, False
        ret = None
        if type(smt.Smt).__name__ == 'ASTBlockSmtNode':
            for smts in smt.Smt.Smt:
                retType, check = self.checkFuncSmt(funcnode, smts)
                if check:
                    if retType != None:
                        if retType == typeclass(typeEnum.NULL):
                            if funcnode.retType.dim > 0:
                                ret = retType
                            elif funcnode.retType.type == typeEnum.CLASS:
                                ret = retType
                            else:
                                return None, False
                        elif retType != funcnode.retType:
                            return None, False
                        else:
                            ret = retType
                else:
                    return None, False
        else:
            ret, check = self.checkFuncSmt(funcnode, smt.Smt)
            if not check:
                return None, False
        self.Scopes.pop()
        return ret, True

    def checkfuncASTLoopWhileNode(self, funcnode, smt):
        self.Scopes.append(Scope(type=ScopeEnum.Loop))
        conditiontype, _, conditioncheck = self.typeget(smt.Condition)
        if conditioncheck and (conditiontype == typeclass(t=typeEnum.BOOL)):
            retType, check = self.checkFuncSmt(funcnode, smt.Smt)
            self.Scopes.pop()
            return retType, check
        return None, False

    def checkclassFuncASTFunctiondeclarationContextNode(self, node):
        self.Scopes.append(Scope(type=ScopeEnum.Func))
        is_return = False
        for arg in node.arglist:
            check = self.check(arg)
            if not check:
                return False
        for i in range(len(node.BlockSmt.Smt)):
            retType, check = self.checkFuncSmt(node, node.BlockSmt.Smt[i])
            if check:
                if retType != None:
                    if retType == typeclass(typeEnum.NULL):
                        if node.retType.dim > 0:
                            is_return = True
                        elif node.retType.type == typeEnum.CLASS:
                            is_return = True
                        else:
                            return False
                    elif retType != node.retType:
                        return False
                    else:
                        is_return = True
            else:
                return False
        if (node.retType != typeclass(t=typeEnum.VOID)) and (not is_return):
            return False
        self.Scopes.pop()
        return True

    def checkASTFunctiondeclarationContextNode(self, node):
        self.Scopes.append(Scope(type=ScopeEnum.Func))
        is_return = False
        for arg in node.arglist:
            check = self.check(arg)
            if not check:
                return False
        for i in range(len(node.BlockSmt.Smt)):

            retType, check = self.checkFuncSmt(node, node.BlockSmt.Smt[i])
            if check:
                if retType != None:
                    if retType == typeclass(typeEnum.NULL):
                        if node.retType.dim > 0:
                            is_return = True
                        elif node.retType.type == typeEnum.CLASS:
                            is_return = True
                        else:
                            return False
                    elif retType != node.retType:
                        return False
                    else:
                        is_return = True
            else:
                return False
        if (node.retType != typeclass(t=typeEnum.VOID)) and (not is_return) and (node.id != 'main'):
            return False
        self.Scopes.pop()
        return True

    def checkASTFuncparamContextNode(self, node):
        if self.typevarscheck(node.type) and (self.checkrepeat(node.id) != len(self.Scopes) - 1):
            self.Scopes[-1].VarsBank[node.id] = node.type
            return True
        return False


if __name__ == "__main__":
    root = os.listdir(sys.argv[1])
    for files in root:
        if files[-3:] == '.mx':
            try:
                print(files + ':', end='')
                input_stream = FileStream(sys.argv[1] + '\\' + files, encoding="utf-8")
                lexer = helloLexer(input_stream)
                lexer._listeners = [MyErrorListener()]
                stream = CommonTokenStream(lexer)
                parser = helloParser(stream)
                parser._listeners = [MyErrorListener()]
                cst = parser.body()
                builder = ASTBuilder()
                ast = builder.build(cst)
                flag = builder.check(ast)
            except Exception as e:
                flag = False

            f5 = open(sys.argv[1] + '\\' + files, encoding="utf-8")
            content = f5.readlines()
            f5.close()
            print(('Verdict: Success\n' in content) == flag)
        elif files[-3:] == 'txt':
            continue
        else:
            subfile = os.listdir(sys.argv[1] + '\\' + files)
            for file in subfile:
                try:
                    print(files + '\\' + file + ':', end='')
                    input_stream = FileStream(sys.argv[1] + '\\' + files + '\\' + file, encoding="utf-8")
                    lexer = helloLexer(input_stream)
                    lexer._listeners = [MyErrorListener()]
                    stream = CommonTokenStream(lexer)
                    parser = helloParser(stream)
                    parser._listeners = [MyErrorListener()]
                    cst = parser.body()
                    builder = ASTBuilder()
                    ast = builder.build(cst)
                    flag = builder.check(ast)
                except Exception as e:
                    flag = False

                f5 = open(sys.argv[1] + '\\' + files + '\\' + file, encoding="utf-8")
                content = f5.readlines()
                f5.close()
                print(('Verdict: Success\n' in content) == flag)

    # try:
    #     input_stream = FileStream(r"C:\Users\14908\Desktop\PPCA\Complier\test.txt", encoding="utf-8")
    #     lexer = helloLexer(input_stream)
    #     lexer._listeners = [MyErrorListener()]
    #     stream = CommonTokenStream(lexer)
    #     parser = helloParser(stream)
    #     parser._listeners = [MyErrorListener()]
    #     cst = parser.body()
    #     builder = ASTBuilder()
    #     ast = builder.build(cst)
    #     flag = builder.check(ast)
    #     print(flag)
    # except Exception as e:
    #     print(e)

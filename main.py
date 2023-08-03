import os
import time

from antlr4 import *
from py_parser.helloLexer import helloLexer
from py_parser.helloParser import helloParser
from enum import Enum
import sys
from antlr4.error.ErrorListener import ErrorListener

output = open('output.ll', 'w')


def getstring(str):
    res = ""
    i = 1
    while (i < len(str) - 1):
        if str[i] != '\\':
            res = res + str[i]
        else:
            if str[i + 1] == '\\':
                res = res + '\\\\'
                i = i + 1
            elif str[i + 1] == 'n':
                res = res + '\\0A'
                i = i + 1
            elif str[i + 1] == '\"':
                res = res + '\\22'
                i = i + 1
            else:
                raise Exception("Error in getstring:", str)
        i = i + 1
    return res


def getstringlength(str):
    res = ""
    i = 1
    size = 0
    while (i < len(str) - 1):
        if str[i] != '\\':
            res = res + str[i]
            size += 1
        else:
            if str[i + 1] == '\\':
                res = res + '\\\\'
                i = i + 1
                size += 1
            elif str[i + 1] == 'n':
                res = res + '\\0A'
                i = i + 1
                size += 1
            elif str[i + 1] == '\"':
                res = res + '\\22'
                i = i + 1
                size += 1
            else:
                raise Exception("Error in getstring:", str)
        i = i + 1
    return size


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
    def __init__(self, type, name="", dim=0, tempvar=0):
        self.VarsBank = {}
        self.type = type
        self.name = name
        self.dim = dim
        self.tempvar = 0


class ClassScope:
    def __init__(self, id="", ClassMember={}, FunctionMember={}):
        self.ClassMember = ClassMember
        self.FunctionMember = FunctionMember
        self.id = id
        self.ConstructFunc = ASTEmptyNode()


class ASTBuilder:
    def __init__(self):
        self.FuncBank = {}
        self.ClassBank = {}
        self.Scopes = [Scope(type=ScopeEnum.Global)]
        self.NameSpace = [Scope(type=ScopeEnum.Global)]
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
        self.globalstring = [""]
        self.llvmfunc = {'__malloc': ['ptr', [['i64', 'buzhidao']], [['entry:\n']]]}
        self.globalvars = []
        self.llvmclass = {}
        self.symbol = {'+': 'add', '-': 'sub', '*': 'mul', '/': 'sdiv', '%': 'srem', '<<': 'shl', '>>': 'ashr', '&': 'and', '^': 'xor',
                       '|': 'or', }
        self.logic = {'==': 'eq', '!=': 'ne', '>': 'sgt', '<': 'slt', '>=': 'sge', '<=': 'sle'}

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
            if node.children[0].children[0].symbol.text not in self.globalstring:
                self.globalstring.append(node.children[0].children[0].symbol.text)
            return ASTConstExprContextNode(typeclass(typeEnum.STRING),
                                           node.children[0].children[0].symbol.text)
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
        res = ASTUnaryExprNode(op=node.op.text, body=self.build(node.children[1]))
        if type(res.body).__name__ == "ASTConstExprContextNode":
            if res.op == '!' and res.body.type == typeclass(t=typeEnum.BOOL):
                return ASTConstExprContextNode(t=typeclass(t=typeEnum.BOOL), v=(not res.body.value))
            elif res.op in ['+', '-', '~'] and res.body.type == typeclass(t=typeEnum.INT):
                return ASTConstExprContextNode(t=typeclass(t=typeEnum.INT), v=eval(res.op + str(res.body.value)))
        return res

    def buildExpExprContext(self, node):
        return ASTBinaryExprNode(op=node.op.text, lhs=self.build(node.lhs), rhs=self.build(node.rhs))

    def buildBinaryExprContext(self, node):
        res = ASTBinaryExprNode(op=node.op.text, lhs=self.build(node.lhs), rhs=self.build(node.rhs))
        if type(res.lhs).__name__ == "ASTConstExprContextNode" and type(res.rhs).__name__ == "ASTConstExprContextNode":
            if res.lhs.type.type == typeEnum.INT and res.rhs.type.type == typeEnum.INT:
                if res.op in ['+', '-', '*', '/', '%', '<<', '>>', '&', '|', '^']:
                    return ASTConstExprContextNode(t=typeclass(t=typeEnum.INT), v=eval(str(res.lhs.value) + res.op + str(res.rhs.value)))
                elif res.op in ['<', '>', '<=', '>=', '==', '!=']:
                    return ASTConstExprContextNode(t=typeclass(t=typeEnum.BOOL), v=eval(str(res.lhs.value) + res.op + str(res.rhs.value)))
            elif res.lhs.type.type == typeEnum.BOOL and res.rhs.type.type == typeEnum.BOOL:
                if res.op == '&&':
                    return ASTConstExprContextNode(t=typeclass(t=typeEnum.BOOL), v=res.lhs.value & res.rhs.value)
                if res.op == '||':
                    return ASTConstExprContextNode(t=typeclass(t=typeEnum.BOOL), v=res.lhs.value | res.rhs.value)
        return res

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
                    self.ClassBank[child.id].ConstructFunc = child.ConstructFunc
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

    def getfuncname(self):
        for i in range(len(self.Scopes) - 1, -1, -1):
            if self.Scopes[i].type == ScopeEnum.Func:
                return self.Scopes[i].name

    def llvm(self, node):
        name = "llvm" + type(node).__name__
        self.__getattribute__(name)(node)

    def llvmASTBodyRootNode(self, node):
        # 先构建类
        for name, classscope in self.ClassBank.items():
            if name != 'int' and name != 'string':
                self.llvm(classscope)
        # 构建所有的常量字符串
        for i in range(len(self.globalstring)):
            self.globalvars.append(
                f"@.str.{i} = global [{getstringlength(self.globalstring[i]) + 1} x i8] c\"{getstring(self.globalstring[i])}\\00\"\n")
        # 构建全局变量
        for child in node.children:
            self.llvm(child)
        for smt in self.globalvars:
            output.write(smt)
        for funcname in self.llvmfunc:
            output.write(f"define {self.llvmfunc[funcname][0]} @{funcname}(")
            for i in range(len(self.llvmfunc[funcname][1])):
                if i != 0:
                    output.write(', ')
                output.write(self.llvmfunc[funcname][1][i][0] + ' ' + self.llvmfunc[funcname][1][i][1])
            output.write("){\n")
            for i in range(len(self.llvmfunc[funcname][2])):
                if len(self.llvmfunc[funcname][2][i]) > 1:
                    for j in range(len(self.llvmfunc[funcname][2][i])):
                        if j != 0:
                            output.write('\t')
                        output.write(self.llvmfunc[funcname][2][i][j])
                    output.write('\n')
            output.write('}\n')

    def llvmClassScope(self, node):
        self.llvmclass[node.id] = []
        res = f"%.CLASS.{node.id} = type " + '{ '
        length = 0
        for id in node.ClassMember:
            self.llvmclass[node.id].append(id)
            if length != 0:
                res = res + ', '
            res = res + self.llvmtypeclass(node.ClassMember[id].type)
            length += 1
        self.globalvars.append(res + ' }\n')
        if self.ClassBank[node.id].ConstructFunc != ASTEmptyNode():
            self.llvmfunc[f".CLASS.{node.id}.{node.id}"] = ['void', [['ptr', '%.this']], [['entry:\n']]]

    def llvmtypeclass(self, typeclass):
        if typeclass.dim > 0:
            return 'ptr'
        elif typeclass.type == typeEnum.CLASS:
            return 'ptr'
        elif typeclass.type == typeEnum.INT:
            return 'i32'
        elif typeclass.type == typeEnum.BOOL:
            return 'i1'
        elif typeclass.type == typeEnum.VOID:
            return 'void'
        elif typeclass.type == typeEnum.STRING:
            return 'ptr'
        elif typeclass.type == typeEnum.NULL:
            return 'ptr'

    def llvmASTClassdeclarationContextNode(self, node):
        pass

    def llvmASTEmptyNode(self, node):
        return

    def llvmASTFunctiondeclarationContextNode(self, node):
        funcname = f"{node.id}"
        self.llvmfunc[funcname] = [self.llvmtypeclass(node.retType), [], [['entry:\n']]]
        self.Scopes.append(Scope(type=ScopeEnum.Func, name=funcname, dim=0, tempvar=0))
        self.NameSpace.append(Scope(type=ScopeEnum.Func, name=funcname, dim=0))
        for arg in node.arglist:
            self.llvmfunc[funcname][1].append([])
            self.llvmfunc[funcname][1][-1].append(self.llvmtypeclass(arg.type))
            self.llvmfunc[funcname][1][-1].append(f"%.{arg.id}")
        for smt in node.BlockSmt.Smt:
            self.llvm(smt)

    def llvmASTVariabledeclarationNode(self, node):
        for inits in node.init:
            self.llvmInit(node.type, inits)

    def llvmInit(self, typetodo, init):
        name = 'llvmInit' + type(init.expr).__name__
        self.__getattribute__(name)(typetodo, init)

    def llvmInitASTConstExprContextNode(self, typetodo, init):
        if self.Scopes[-1].type == ScopeEnum.Global:
            if init.expr.type.type in [typeEnum.INT, typeEnum.BOOL]:
                self.globalvars.append(f"@.{init.id} = global {self.llvmtypeclass(typetodo)} {int(init.expr.value)}\n")
                self.NameSpace[-1].VarsBank[init.id] = f"@.{init.id}"
                self.NameSpace[-1].VarsBank[f"@.{init.id}"] = f"@.{init.id}"
                self.Scopes[-1].VarsBank[init.id] = typetodo
            elif init.expr.type.type == typeEnum.STRING:
                self.globalvars.append(f"@.{init.id} = global ptr @.str.{self.globalstring.index(init.expr.value)}\n")
                self.NameSpace[-1].VarsBank[init.id] = f"@.{init.id}"
                self.NameSpace[-1].VarsBank[f"@.{init.id}"] = f"@.{init.id}"
                self.Scopes[-1].VarsBank[init.id] = typetodo
            elif init.expr.type.type == typeEnum.NULL:
                self.globalvars.append(f"@.{init.id} = global ptr null\n")
                self.NameSpace[-1].VarsBank[init.id] = f"@.{init.id}"
                self.NameSpace[-1].VarsBank[f"@.{init.id}"] = f"@.{init.id}"
                self.Scopes[-1].VarsBank[init.id] = typetodo
        else:
            where = self.llvmfunc[self.getfuncname()][2][self.Scopes[-1].dim]
            varname = f"%.{init.id}.{len(self.Scopes)}.{self.Scopes[-1].dim}"
            self.NameSpace[-1].VarsBank[init.id] = varname
            self.NameSpace[-1].VarsBank[varname] = varname
            self.Scopes[-1].VarsBank[init.id] = typetodo
            if typetodo.type in [typeEnum.INT, typeEnum.BOOL]:
                self.generatealloca(where, typetodo, varname)
                self.generatestore(where, typetodo, init.id, str(int(init.expr.value)))
            elif typetodo.type == typeEnum.STRING:
                self.generatealloca(where, typetodo, varname)
                self.generatestore(where, typetodo, init.id, f"@.str.{self.globalstring.index(init.expr.value)}")
            elif typetodo.type == typeEnum.NULL:
                self.generatealloca(where, typetodo, varname)
                self.generatestore(where, typetodo, init.id, f"null")

    def getelementptr(self, node):
        where = self.llvmfunc[self.getfuncname()][2][self.Scopes[-1].dim]
        if type(node).__name__ == "ASTIdentifierExprNode":
            return self.getname(node.id)
        elif type(node).__name__ == "ASTPrefixUpdateExprNode":
            bodyptr = self.getelementptr(node.body)
            newvar = f"%._{self.Scopes[-1].tempvar}"
            self.Scopes[-1].tempvar += 1
            self.generateload(where, typeclass(t=typeEnum.INT), bodyptr, newvar)
            newvars = f"%._{self.Scopes[-1].tempvar}"
            self.Scopes[-1].tempvar += 1
            if node.op == '++':
                self.generateFuncCall(where, None, '+', [newvar, '1'], newvars)
            else:
                self.generateFuncCall(where, None, '-', [newvar, '1'], newvars)
            self.generatestore(where, typeclass(t=typeEnum.INT), bodyptr, newvars)
            return bodyptr
        else:
            raise Exception("TODO")

    def llvmInitASTPostfixUpdateExprNode(self, typetodo, init):
        if self.Scopes[-1].type == ScopeEnum.Global:
            self.globalvars.append(f"@.{init.id} = global i32 0\n")
            self.NameSpace[-1].VarsBank[init.id] = f"@.{init.id}"
            self.NameSpace[-1].VarsBank[f"@.{init.id}"] = f"@.{init.id}"
            self.Scopes[-1].VarsBank[init.id] = typetodo
            funcname = f'_init.{len(self.llvmfunc)}'
            self.Scopes.append(Scope(type=ScopeEnum.Func, name=funcname, dim=0, tempvar=0))
            self.NameSpace.append(Scope(ScopeEnum.Func))
            self.llvmfunc[funcname] = ['void', [], [['entry:\n']]]
            bodyptr = self.getelementptr(init.expr.body)
            newvar = f"%._{self.Scopes[-1].tempvar}"
            self.Scopes[-1].tempvar += 1
            self.generateload(self.llvmfunc[funcname][2][0], typetodo, bodyptr, newvar)
            self.generatestore(self.llvmfunc[funcname][2][0], typetodo, init.id, newvar)
            newvars = f"%._{self.Scopes[-1].tempvar}"
            self.Scopes[-1].tempvar += 1
            if init.expr.op == '++':
                self.generateFuncCall(self.llvmfunc[funcname][2][0], None, '+', [newvar, '1'], newvars)
            else:
                self.generateFuncCall(self.llvmfunc[funcname][2][0], None, '-', [newvar, '1'], newvars)
            self.generatestore(self.llvmfunc[funcname][2][0], typeclass(t=typeEnum.INT), bodyptr, newvars)
            self.generateret(self.llvmfunc[funcname][2][0], typeclass(t=typeEnum.VOID), ASTEmptyNode())
            self.Scopes.pop()
            self.NameSpace.pop()
        else:
            where = self.llvmfunc[self.getfuncname()][2][self.Scopes[-1].dim]
            varname = f"%.{init.id}.{len(self.Scopes)}.{self.Scopes[-1].dim}"
            self.NameSpace[-1].VarsBank[init.id] = varname
            self.NameSpace[-1].VarsBank[varname] = varname
            self.Scopes[-1].VarsBank[init.id] = typetodo
            self.generatealloca(where, typetodo, varname)
            bodyptr = self.getelementptr(init.expr.body)
            newvar = f"%._{self.Scopes[-1].tempvar}"
            self.Scopes[-1].tempvar += 1
            self.generateload(where, typetodo, bodyptr, newvar)
            self.generatestore(where, typetodo, init.id, newvar)
            newvars = f"%._{self.Scopes[-1].tempvar}"
            self.Scopes[-1].tempvar += 1
            if init.expr.op == '++':
                self.generateFuncCall(where, None, '+', [newvar, '1'], newvars)
            else:
                self.generateFuncCall(where, None, '-', [newvar, '1'], newvars)
            self.generatestore(where, typeclass(t=typeEnum.INT), bodyptr, newvars)

    def llvmInitASTPrefixUpdateExprNode(self, typetodo, init):
        if self.Scopes[-1].type == ScopeEnum.Global:
            self.globalvars.append(f"@.{init.id} = global i32 0\n")
            self.NameSpace[-1].VarsBank[init.id] = f"@.{init.id}"
            self.NameSpace[-1].VarsBank[f"@.{init.id}"] = f"@.{init.id}"
            self.Scopes[-1].VarsBank[init.id] = typetodo
            funcname = f'_init.{len(self.llvmfunc)}'
            self.Scopes.append(Scope(type=ScopeEnum.Func, name=funcname, dim=0, tempvar=0))
            self.NameSpace.append(Scope(ScopeEnum.Func))
            self.llvmfunc[funcname] = ['void', [], [['entry:\n']]]
            bodyptr = self.getelementptr(init.expr.body)
            newvar = f"%._{self.Scopes[-1].tempvar}"
            self.Scopes[-1].tempvar += 1
            self.generateload(self.llvmfunc[funcname][2][0], typetodo, newvar, bodyptr)
            newvars = f"%._{self.Scopes[-1].tempvar}"
            self.Scopes[-1].tempvar += 1
            if init.expr.op == '++':
                self.generateFuncCall(self.llvmfunc[funcname][2][0], None, '+', [newvar, '1'], newvars)
            else:
                self.generateFuncCall(self.llvmfunc[funcname][2][0], None, '-', [newvar, '1'], newvars)
            self.generatestore(self.llvmfunc[funcname][2][0], typeclass(t=typeEnum.INT), bodyptr, newvars)
            self.generatestore(self.llvmfunc[funcname][2][0], typeclass(t=typeEnum.INT), init.id, newvars)
            self.generateret(self.llvmfunc[funcname][2][0], typeclass(t=typeEnum.VOID), ASTEmptyNode())
            self.Scopes.pop()
            self.NameSpace.pop()
        else:
            where = self.llvmfunc[self.getfuncname()][2][self.Scopes[-1].dim]
            varname = f"%.{init.id}.{len(self.Scopes)}.{self.Scopes[-1].dim}"
            self.NameSpace[-1].VarsBank[init.id] = varname
            self.NameSpace[-1].VarsBank[varname] = varname
            self.Scopes[-1].VarsBank[init.id] = typetodo
            self.generatealloca(where, typetodo, varname)
            bodyptr = self.getelementptr(init.expr.body)
            newvar = f"%._{self.Scopes[-1].tempvar}"
            self.Scopes[-1].tempvar += 1
            self.generateload(where, typetodo, bodyptr, newvar)

            newvars = f"%._{self.Scopes[-1].tempvar}"
            self.Scopes[-1].tempvar += 1
            if init.expr.op == '++':
                self.generateFuncCall(where, None, '+', [newvar, '1'], newvars)
            else:
                self.generateFuncCall(where, None, '-', [newvar, '1'], newvars)
            self.generatestore(where, typeclass(t=typeEnum.INT), bodyptr, newvars)
            self.generatestore(where, typeclass(t=typeEnum.INT), init.id, newvars)

    def llvmInitASTEmptyNode(self, typetodo, init):
        if self.Scopes[-1].type == ScopeEnum.Global:
            if typetodo.type in [typeEnum.INT, typeEnum.BOOL]:
                self.globalvars.append(f"@.{init.id} = global {self.llvmtypeclass(typetodo)} 0\n")
                self.NameSpace[-1].VarsBank[init.id] = f"@.{init.id}"
                self.NameSpace[-1].VarsBank[f"@.{init.id}"] = f"@.{init.id}"
                self.Scopes[-1].VarsBank[init.id] = typetodo
            elif typetodo.type == typeEnum.STRING:
                self.globalvars.append(f"@.{init.id} = global ptr @.str.{self.globalstring.index('')}\n")
                self.NameSpace[-1].VarsBank[init.id] = f"@.{init.id}"
                self.NameSpace[-1].VarsBank[f"@.{init.id}"] = f"@.{init.id}"
                self.Scopes[-1].VarsBank[init.id] = typetodo
            elif typetodo.type == typeEnum.CLASS:
                self.globalvars.append(f"@.{init.id} = global ptr null\n")
                self.NameSpace[-1].VarsBank[init.id] = f"@.{init.id}"
                self.NameSpace[-1].VarsBank[f"@.{init.id}"] = f"@.{init.id}"
                self.Scopes[-1].VarsBank[init.id] = typetodo
        else:
            where = self.llvmfunc[self.getfuncname()][2][self.Scopes[-1].dim]
            varname = f"%.{init.id}.{len(self.Scopes)}.{self.Scopes[-1].dim}"
            self.NameSpace[-1].VarsBank[init.id] = varname
            self.NameSpace[-1].VarsBank[varname] = varname
            self.Scopes[-1].VarsBank[init.id] = typetodo
            if typetodo.type in [typeEnum.INT, typeEnum.BOOL]:
                self.generatealloca(where, typetodo, varname)
                self.generatestore(where, typetodo, init.id, '0')
            elif typetodo.type == typeEnum.STRING:
                self.generatealloca(where, typetodo, varname)
                self.generatestore(where, typetodo, init.id, f"@.str.{self.globalstring.index('')}")
            elif typetodo.type == typeEnum.CLASS:
                self.generatealloca(where, typetodo, varname)
                self.generatestore(where, typetodo, init.id, f"null")

    def llvmInitASTIdentifierExprNode(self, typetodo, init):
        if self.Scopes[-1].type == ScopeEnum.Global:
            if typetodo.type in [typeEnum.INT, typeEnum.BOOL]:
                self.globalvars.append(f"@.{init.id} = global {self.llvmtypeclass(typetodo)} 0\n")
                self.NameSpace[-1].VarsBank[init.id] = f"@.{init.id}"
                self.NameSpace[-1].VarsBank[f"@.{init.id}"] = f"@.{init.id}"
                self.Scopes[-1].VarsBank[init.id] = typetodo
                funcname = f'_init.{len(self.llvmfunc)}'
                self.Scopes.append(Scope(type=ScopeEnum.Func, name=funcname, dim=0, tempvar=0))
                self.NameSpace.append(Scope(ScopeEnum.Func))
                self.llvmfunc[funcname] = ['void', [], [['entry:\n']]]
                self.generatestore(self.llvmfunc[funcname][2][0], typetodo, init.id, init.expr)
                self.generateret(self.llvmfunc[funcname][2][0], typeclass(t=typeEnum.VOID), ASTEmptyNode())
                self.Scopes.pop()
                self.NameSpace.pop()
            elif typetodo.type in [typeEnum.STRING, typeEnum.CLASS]:
                self.globalvars.append(f"@.{init.id} = global ptr null\n")
                self.NameSpace[-1].VarsBank[init.id] = f"@.{init.id}"
                self.NameSpace[-1].VarsBank[f"@.{init.id}"] = f"@.{init.id}"
                self.Scopes[-1].VarsBank[init.id] = typetodo
                funcname = f'_init.{len(self.llvmfunc)}'
                self.Scopes.append(Scope(type=ScopeEnum.Func, name=funcname, dim=0, tempvar=0))
                self.NameSpace.append(Scope(ScopeEnum.Func))
                self.llvmfunc[funcname] = ['void', [], [['entry:\n']]]
                self.generatestore(self.llvmfunc[funcname][2][0], typetodo, init.id, init.expr)
                self.generateret(self.llvmfunc[funcname][2][0], typeclass(t=typeEnum.VOID), ASTEmptyNode())
                self.Scopes.pop()
                self.NameSpace.pop()
        else:
            where = self.llvmfunc[self.getfuncname()][2][self.Scopes[-1].dim]
            varname = f"%.{init.id}.{len(self.Scopes)}.{self.Scopes[-1].dim}"
            self.NameSpace[-1].VarsBank[init.id] = varname
            self.NameSpace[-1].VarsBank[varname] = varname
            self.Scopes[-1].VarsBank[init.id] = typetodo
            if typetodo.type in [typeEnum.INT, typeEnum.BOOL]:
                self.generatealloca(where, typetodo, varname)
                self.generatestore(where, typetodo, init.id, init.expr)
            elif typetodo.type == typeEnum.STRING:
                self.generatealloca(where, typetodo, varname)
                self.generatestore(where, typetodo, init.id, init.expr)
            elif typetodo.type == typeEnum.CLASS:
                raise Exception("TODO")

    def llvmInitASTNewClassNode(self, typetodo, init):
        if self.Scopes[-1].type == ScopeEnum.Global:
            self.globalvars.append(f"@.{init.id} = global ptr null\n")
            self.NameSpace[-1].VarsBank[init.id] = f"@.{init.id}"
            self.NameSpace[-1].VarsBank[f"@.{init.id}"] = f"@.{init.id}"
            self.Scopes[-1].VarsBank[init.id] = typetodo
            funcname = f'_init.{len(self.llvmfunc)}'
            self.Scopes.append(Scope(type=ScopeEnum.Func, name=funcname, dim=0, tempvar=0))
            self.NameSpace.append(Scope(ScopeEnum.Func))
            self.llvmfunc[funcname] = ['void', [], [['entry:\n']]]
            self.generatestore(self.llvmfunc[funcname][2][0], typetodo, init.id, init.expr)
            if self.ClassBank[typetodo.name].ConstructFunc != ASTEmptyNode():
                self.generateFuncCall(self.llvmfunc[funcname][2][0], typeclass(t=typeEnum.VOID), f".CLASS.{typetodo.name}.{typetodo.name}", [init.id], None)
            self.generateret(self.llvmfunc[funcname][2][0], typeclass(t=typeEnum.VOID), ASTEmptyNode())
            self.Scopes.pop()
            self.NameSpace.pop()
        else:
            where = self.llvmfunc[self.getfuncname()][2][self.Scopes[-1].dim]
            varname = f"%.{init.id}.{len(self.Scopes)}.{self.Scopes[-1].dim}"
            self.NameSpace[-1].VarsBank[init.id] = varname
            self.NameSpace[-1].VarsBank[varname] = varname
            self.Scopes[-1].VarsBank[init.id] = typetodo
            self.generatealloca(where, typetodo, varname)
            self.generatestore(where, typetodo, init.id, init.expr)
            if self.ClassBank[typetodo.name].ConstructFunc != ASTEmptyNode():
                self.generateFuncCall(where, typeclass(t=typeEnum.VOID), f".CLASS.{typetodo.name}.{typetodo.name}", [init.id], None)

    def llvmInitASTMemberVarExprNode(self, typetodo, init):
        if self.Scopes[-1].type == ScopeEnum.Global:
            if typetodo.type in [typeEnum.INT, typeEnum.BOOL]:
                self.globalvars.append(f"@.{init.id} = global {self.llvmtypeclass(typetodo)} 0\n")
                self.NameSpace[-1].VarsBank[init.id] = f"@.{init.id}"
                self.NameSpace[-1].VarsBank[f"@.{init.id}"] = f"@.{init.id}"
                self.Scopes[-1].VarsBank[init.id] = typetodo
            elif typetodo.type == typeEnum.STRING:
                self.globalvars.append(f"@.{init.id} = global ptr @.str.{self.globalstring.index('')}\n")
                self.NameSpace[-1].VarsBank[init.id] = f"@.{init.id}"
                self.NameSpace[-1].VarsBank[f"@.{init.id}"] = f"@.{init.id}"
                self.Scopes[-1].VarsBank[init.id] = typetodo
            elif typetodo.type == typeEnum.CLASS:
                self.globalvars.append(f"@.{init.id} = global ptr null\n")
                self.NameSpace[-1].VarsBank[init.id] = f"@.{init.id}"
                self.NameSpace[-1].VarsBank[f"@.{init.id}"] = f"@.{init.id}"
                self.Scopes[-1].VarsBank[init.id] = typetodo
            funcname = f'_init.{len(self.llvmfunc)}'
            self.Scopes.append(Scope(type=ScopeEnum.Func, name=funcname, dim=0, tempvar=0))
            self.NameSpace.append(Scope(ScopeEnum.Func))
            self.llvmfunc[funcname] = ['void', [], [['entry:\n']]]
            if type(init.expr.body).__name__ != "ASTIdentifierExprNode":
                newvar = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.NameSpace[-1].VarsBank[newvar] = newvar
                self.Scopes[-1].VarsBank[newvar] = self.typeget(init.expr.body)[0]
                self.generateload(self.llvmfunc[funcname][2][0], self.typeget(init.expr.body)[0], init.expr.body, newvar)
                newvar = self.generategetelementptr(self.llvmfunc[funcname][2][0], self.Scopes[-1].VarsBank[newvar], newvar, init.expr.id)
            else:
                newvar = self.generategetelementptr(self.llvmfunc[funcname][2][0], self.typeget(init.expr.body)[0], self.getname(init.expr.body.id),
                                                    init.expr.id)
            if typetodo.type in [typeEnum.INT, typeEnum.BOOL]:
                newvars = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.NameSpace[-1].VarsBank[newvars] = newvars
                self.Scopes[-1].VarsBank[newvars] = typetodo
                self.generateload(self.llvmfunc[funcname][2][0], self.Scopes[-1].VarsBank[newvar], newvar, newvars)
                newvar = newvars
            self.generatestore(self.llvmfunc[funcname][2][0], typetodo, init.id, newvar)
            self.generateret(self.llvmfunc[funcname][2][0], typeclass(t=typeEnum.VOID), ASTEmptyNode())
            self.Scopes.pop()
            self.NameSpace.pop()
        else:
            where = self.llvmfunc[self.getfuncname()][2][self.Scopes[-1].dim]
            varname = f"%.{init.id}.{len(self.Scopes)}.{self.Scopes[-1].dim}"
            self.NameSpace[-1].VarsBank[init.id] = varname
            self.NameSpace[-1].VarsBank[varname] = varname
            self.Scopes[-1].VarsBank[init.id] = typetodo
            self.generatealloca(where, typetodo, varname)
            if type(init.expr.body).__name__ != "ASTIdentifierExprNode":
                newvar = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.NameSpace[-1].VarsBank[newvar] = newvar
                self.Scopes[-1].VarsBank[newvar] = self.typeget(init.expr.body)[0]
                self.generateload(where, self.typeget(init.expr.body)[0], init.expr.body, newvar)
                newvar = self.generategetelementptr(where, self.Scopes[-1].VarsBank[newvar], newvar, init.expr.id)
            else:
                newvar = self.generategetelementptr(where, self.typeget(init.expr.body)[0], self.getname(init.expr.body.id), init.expr.id)
            if typetodo.type in [typeEnum.INT, typeEnum.BOOL]:
                newvars = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.NameSpace[-1].VarsBank[newvars] = newvars
                self.Scopes[-1].VarsBank[newvars] = typetodo
                self.generateload(where, self.Scopes[-1].VarsBank[newvar], newvar, newvars)
                newvar = newvars
            self.generatestore(where, typetodo, init.id, newvar)

    def llvmInitASTBinaryExprNode(self, typetodo, init):
        if self.Scopes[-1].type == ScopeEnum.Global:
            if typetodo.type == typeEnum.INT:
                self.globalvars.append(f"@.{init.id} = global {self.llvmtypeclass(typetodo)} 0\n")
                self.NameSpace[-1].VarsBank[init.id] = f"@.{init.id}"
                self.NameSpace[-1].VarsBank[f"@.{init.id}"] = f"@.{init.id}"
                self.Scopes[-1].VarsBank[init.id] = typetodo
                funcname = f'_init.{len(self.llvmfunc)}'
                self.Scopes.append(Scope(type=ScopeEnum.Func, name=funcname, dim=0, tempvar=0))
                self.NameSpace.append(Scope(ScopeEnum.Func))
                self.llvmfunc[funcname] = ['void', [], [['entry:\n']]]
                if type(init.expr.lhs).__name__ == "ASTConstExprContextNode":
                    lhsnewvar = str(init.expr.lhs.value)
                else:
                    lhsnewvar = f"%._{self.Scopes[-1].tempvar}"
                    self.Scopes[-1].tempvar += 1
                    self.NameSpace[-1].VarsBank[lhsnewvar] = lhsnewvar
                    self.Scopes[-1].VarsBank[lhsnewvar] = typetodo
                    self.generateload(self.llvmfunc[funcname][2][0], typetodo, init.expr.lhs, lhsnewvar)
                if type(init.expr.rhs).__name__ == "ASTConstExprContextNode":
                    rhsnewvar = str(init.expr.rhs.value)
                else:
                    rhsnewvar = f"%._{self.Scopes[-1].tempvar}"
                    self.Scopes[-1].tempvar += 1
                    self.NameSpace[-1].VarsBank[rhsnewvar] = rhsnewvar
                    self.Scopes[-1].VarsBank[rhsnewvar] = typetodo
                    self.generateload(self.llvmfunc[funcname][2][0], typetodo, init.expr.rhs, rhsnewvar)
                var = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.generateFuncCall(self.llvmfunc[funcname][2][0], None, init.expr.op, [lhsnewvar, rhsnewvar], var)
                self.generatestore(self.llvmfunc[funcname][2][0], typetodo, init.id, var)
                self.generateret(self.llvmfunc[funcname][2][0], typeclass(t=typeEnum.VOID), ASTEmptyNode())
                self.Scopes.pop()
                self.NameSpace.pop()
            # 短路求值TODO
        else:
            where = self.llvmfunc[self.getfuncname()][2][self.Scopes[-1].dim]
            varname = f"%.{init.id}.{len(self.Scopes)}.{self.Scopes[-1].dim}"
            self.NameSpace[-1].VarsBank[init.id] = varname
            self.NameSpace[-1].VarsBank[varname] = varname
            self.Scopes[-1].VarsBank[init.id] = typetodo
            self.generatealloca(where, typetodo, varname)
            if typetodo.type == typeEnum.INT:
                if type(init.expr.lhs).__name__ == "ASTConstExprContextNode":
                    lhsnewvar = str(init.expr.lhs.value)
                else:
                    lhsnewvar = f"%._{self.Scopes[-1].tempvar}"
                    self.Scopes[-1].tempvar += 1
                    self.NameSpace[-1].VarsBank[lhsnewvar] = lhsnewvar
                    self.Scopes[-1].VarsBank[lhsnewvar] = typetodo
                    self.generateload(where, typetodo, init.expr.lhs, lhsnewvar)
                if type(init.expr.rhs).__name__ == "ASTConstExprContextNode":
                    rhsnewvar = str(init.expr.rhs.value)
                else:
                    rhsnewvar = f"%._{self.Scopes[-1].tempvar}"
                    self.Scopes[-1].tempvar += 1
                    self.NameSpace[-1].VarsBank[rhsnewvar] = rhsnewvar
                    self.Scopes[-1].VarsBank[rhsnewvar] = typetodo
                    self.generateload(where, typetodo, init.expr.rhs, rhsnewvar)
                var = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.generateFuncCall(where, None, init.expr.op, [lhsnewvar, rhsnewvar], var)
                self.generatestore(where, typetodo, init.id, var)

    def llvmInitASTUnaryExprNode(self, typetodo, init):
        if self.Scopes[-1].type == ScopeEnum.Global:
            self.globalvars.append(f"@.{init.id} = global {self.llvmtypeclass(typetodo)} 0\n")
            self.NameSpace[-1].VarsBank[init.id] = f"@.{init.id}"
            self.NameSpace[-1].VarsBank[f"@.{init.id}"] = f"@.{init.id}"
            self.Scopes[-1].VarsBank[init.id] = typetodo
            funcname = f'_init.{len(self.llvmfunc)}'
            self.Scopes.append(Scope(type=ScopeEnum.Func, name=funcname, dim=0, tempvar=0))
            self.NameSpace.append(Scope(ScopeEnum.Func))
            self.llvmfunc[funcname] = ['void', [], [['entry:\n']]]
            if init.expr.op == '+':
                newvar = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.generateload(self.llvmfunc[funcname][2][0], typetodo, init.expr.body, newvar)
                self.generatestore(self.llvmfunc[funcname][2][0], typetodo, init.id, newvar)
            elif init.expr.op == '-':
                newvar = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.generateload(self.llvmfunc[funcname][2][0], typetodo, init.expr.body, newvar)
                var = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.generateFuncCall(self.llvmfunc[funcname][2][0], None, '-', ['0', newvar], var)
                self.generatestore(self.llvmfunc[funcname][2][0], typetodo, init.id, var)
            elif init.expr.op == '~':
                newvar = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.generateload(self.llvmfunc[funcname][2][0], typetodo, init.expr.body, newvar)
                var = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.generateFuncCall(self.llvmfunc[funcname][2][0], None, '^', [newvar, '-1'], var)
                self.generatestore(self.llvmfunc[funcname][2][0], typetodo, init.id, var)
            elif init.expr.op == '!':
                newvar = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.generateload(self.llvmfunc[funcname][2][0], typetodo, init.expr.body, newvar)
                var = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.generateFuncCall(self.llvmfunc[funcname][2][0], None, '!', [newvar, 'true'], var)
                self.generatestore(self.llvmfunc[funcname][2][0], typetodo, init.id, var)
            self.generateret(self.llvmfunc[funcname][2][0], typeclass(t=typeEnum.VOID), ASTEmptyNode())
            self.Scopes.pop()
            self.NameSpace.pop()
        else:
            where = self.llvmfunc[self.getfuncname()][2][self.Scopes[-1].dim]
            varname = f"%.{init.id}.{len(self.Scopes)}.{self.Scopes[-1].dim}"
            self.NameSpace[-1].VarsBank[init.id] = varname
            self.NameSpace[-1].VarsBank[varname] = varname
            self.Scopes[-1].VarsBank[init.id] = typetodo
            self.generatealloca(where, typetodo, varname)
            if init.expr.op == '+':
                newvar = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.generateload(where, typetodo, init.expr.body, newvar)
                self.generatestore(where, typetodo, init.id, newvar)
            elif init.expr.op == '-':
                newvar = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.generateload(where, typetodo, init.expr.body, newvar)
                var = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.generateFuncCall(where, None, '-', ['0', newvar], var)
                self.generatestore(where, typetodo, init.id, var)
            elif init.expr.op == '~':
                newvar = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.generateload(where, typetodo, init.expr.body, newvar)
                var = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.generateFuncCall(where, None, '^', [newvar, '-1'], var)
                self.generatestore(where, typetodo, init.id, var)
            elif init.expr.op == '!':
                newvar = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.generateload(where, typetodo, init.expr.body, newvar)
                var = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.generateFuncCall(where, None, '!', [newvar, 'true'], var)
                self.generatestore(where, typetodo, init.id, var)

    def llvmASTPostfixUpdateExprNode(self, node):
        where = self.llvmfunc[self.getfuncname()][2][self.Scopes[-1].dim]
        bodytpr = self.getelementptr(node.body)
        self.generateload(where, typeclass(t=typeEnum.INT), bodytpr, newvar)
        newvars = f"%._{self.Scopes[-1].tempvar}"
        self.Scopes[-1].tempvar += 1
        if node.op == '++':
            self.generateFuncCall(where, None, '+', [newvar, '1'], newvars)
        else:
            self.generateFuncCall(where, None, '-', [newvar, '1'], newvars)
        self.generatestore(where, typeclass(t=typeEnum.INT), bodytpr, newvars)

    def llvmASTPrefixUpdateExprNode(self, node):
        where = self.llvmfunc[self.getfuncname()][2][self.Scopes[-1].dim]
        bodytpr = self.getelementptr(node.body)
        self.generateload(where, typeclass(t=typeEnum.INT), bodytpr, newvar)
        newvars = f"%._{self.Scopes[-1].tempvar}"
        self.Scopes[-1].tempvar += 1
        if node.op == '++':
            self.generateFuncCall(where, None, '+', [newvar, '1'], newvars)
        else:
            self.generateFuncCall(where, None, '-', [newvar, '1'], newvars)
        self.generatestore(where, typeclass(t=typeEnum.INT), bodytpr, newvars)

    def llvmASTControlNode(self, node):
        where = self.llvmfunc[self.getfuncname()][2][self.Scopes[-1].dim]
        if node.cmd == 'Return':
            if node.returnExpr == ASTEmptyNode():
                self.generateret(where, typeclass(t=typeEnum.VOID), None)
            elif type(node.returnExpr).__name__ == "ASTConstExprContextNode":
                self.generateret(where, self.typeget(node.returnExpr)[0], str(int(node.returnExpr.value)))
            else:
                newvar = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.generateload(where, self.typeget(node.returnExpr)[0], node.returnExpr, newvar)
                self.generateret(where, self.typeget(node.returnExpr)[0], newvar)

        else:
            raise Exception("TODO")

    def llvmASTBranchStatementNode(self, node):
        root = self.llvmfunc[self.getfuncname()][2]
        if type(node.condition).__name__ == "ASTConstExprContextNode":
            if node.condition.value and ((node.ifSmt != ASTEmptyNode()) and (type(node.ifSmt).__name__ != "ASTBlockSmtNode" or (len(node.ifSmt.Smt) != 0))):
                ifSmtind = len(root)
                ifSmt = f"ifSmt.{len(root)}"
                root.append([f'ifSmt.{len(root)}:\n'])
                endSmtind = len(root)
                endSmt = f"ifendSmt.{len(root)}"
                root.append([f'ifendSmt.{len(root)}:\n'])
                self.generatejump(root[self.Scopes[-1].dim], ifSmt)
                self.Scopes.append(Scope(type=ScopeEnum.Loop, name='', dim=self.Scopes[-1].dim, tempvar=self.Scopes[-1].tempvar))
                self.NameSpace.append(Scope(type=ScopeEnum.Loop, name='', dim=self.Scopes[-1].dim, tempvar=0))
                self.Scopes[-1].dim = ifSmtind
                self.Scopes[-1].tempvar = self.Scopes[-2].tempvar
                if type(node.ifSmt).__name__ == "ASTBlockSmtNode":
                    for smt in node.ifSmt.Smt:
                        self.llvm(smt)
                else:
                    self.llvm(node.ifSmt)
                self.generatejump(root[self.Scopes[-1].dim], endSmt)
                self.Scopes[-2].dim = endSmtind
                self.Scopes[-2].tempvar = self.Scopes[-1].tempvar
                self.Scopes.pop()
                self.NameSpace.pop()
            if not node.condition.value and (
                    (node.elseSmt != ASTEmptyNode()) and (type(node.elseSmt).__name__ != "ASTBlockSmtNode" or (len(node.elseSmt.Smt) != 0))):
                elseSmtind = len(root)
                elseSmt = f"ifSmt.{len(root)}"
                root.append([f'elseSmt.{len(root)}:\n'])
                endSmtind = len(root)
                endSmt = f"ifendSmt.{len(root)}"
                root.append([f'ifendSmt.{len(root)}:\n'])
                self.generatejump(root[self.Scopes[-1].dim], elseSmt)
                self.Scopes.append(Scope(type=ScopeEnum.Loop, name='', dim=self.Scopes[-1].dim, tempvar=self.Scopes[-1].tempvar))
                self.NameSpace.append(Scope(type=ScopeEnum.Loop, name='', dim=self.Scopes[-1].dim, tempvar=0))
                self.Scopes[-1].dim = elseSmtind
                self.Scopes[-1].tempvar = self.Scopes[-2].tempvar
                if type(node.elseSmt).__name__ == "ASTBlockSmtNode":
                    for smt in node.elseSmt.Smt:
                        self.llvm(smt)
                else:
                    self.llvm(node.elseSmt)
                self.generatejump(root[self.Scopes[-1].dim], endSmt)
                self.Scopes[-2].dim = endSmtind
                self.Scopes[-2].tempvar = self.Scopes[-1].tempvar
                self.Scopes.pop()
                self.NameSpace.pop()
        else:
            newvar = f"%._{self.Scopes[-1].tempvar}"
            self.Scopes[-1].tempvar += 1
            self.generateload(root[self.Scopes[-1].dim], typeclass(t=typeEnum.BOOL), node.condition, newvar)
            if node.ifSmt != ASTEmptyNode():
                ifSmtind = len(root)
                ifSmt = f"ifSmt.{len(root)}"
                root.append([f'ifSmt.{len(root)}:\n'])
            else:
                ifSmtind = -1
            if node.elseSmt != ASTEmptyNode():
                elseSmtind = len(root)
                elseSmt = f"elseSmt.{len(root)}"
                root.append([f'elseSmt.{len(root)}:\n'])
                endSmtind = len(root)
                endSmt = f"ifendSmt.{len(root)}"
                root.append([f'ifendSmt.{len(root)}:\n'])
                self.generatebranch(root[self.Scopes[-1].dim], newvar, ifSmt, elseSmt)
            else:
                endSmtind = len(root)
                endSmt = f"ifendSmt.{len(root)}"
                root.append([f'ifendSmt.{len(root)}:\n'])
                elseSmtind = -1
                self.generatebranch(root[self.Scopes[-1].dim], newvar, ifSmt, endSmt)

            if ifSmtind != -1:
                self.Scopes.append(Scope(type=ScopeEnum.Loop, name='', dim=self.Scopes[-1].dim, tempvar=self.Scopes[-1].tempvar))
                self.NameSpace.append(Scope(type=ScopeEnum.Loop, name='', dim=self.Scopes[-1].dim, tempvar=0))
                self.Scopes[-1].dim = ifSmtind
                self.Scopes[-1].tempvar = self.Scopes[-2].tempvar
                if type(node.ifSmt).__name__ == "ASTBlockSmtNode":
                    for smt in node.ifSmt.Smt:
                        self.llvm(smt)
                else:
                    self.llvm(node.ifSmt)
                self.generatejump(root[self.Scopes[-1].dim], endSmt)
                self.Scopes[-2].dim = self.Scopes[-1].dim
                self.Scopes[-2].tempvar = self.Scopes[-1].tempvar
                self.Scopes.pop()
                self.NameSpace.pop()
            if elseSmtind != -1:
                self.Scopes.append(Scope(type=ScopeEnum.Loop, name='', dim=self.Scopes[-1].dim, tempvar=self.Scopes[-1].tempvar))
                self.NameSpace.append(Scope(type=ScopeEnum.Loop, name='', dim=self.Scopes[-1].dim, tempvar=0))
                self.Scopes[-1].dim = elseSmtind
                self.Scopes[-1].tempvar = self.Scopes[-2].tempvar
                if type(node.elseSmt).__name__ == "ASTBlockSmtNode":
                    for smt in node.elseSmt.Smt:
                        self.llvm(smt)
                else:
                    self.llvm(node.elseSmt)
                self.generatejump(root[self.Scopes[-1].dim], endSmt)
                self.Scopes[-2].dim = self.Scopes[-1].dim
                self.Scopes[-2].tempvar = self.Scopes[-1].tempvar
                self.Scopes.pop()
                self.NameSpace.pop()
            self.Scopes[-1].dim = endSmtind

    def llvmASTAssignExprNode(self, node):
        where = self.llvmfunc[self.getfuncname()][2][self.Scopes[-1].dim]
        if type(node.rhs).__name__ != "ASTConstExprContextNode":
            newvar = f"%._{self.Scopes[-1].tempvar}"
            self.Scopes[-1].tempvar += 1
            self.generateload(where, self.typeget(node.rhs)[0], node.rhs, newvar)
        else:
            newvar = str(int(node.rhs.value))
        lhsptr = self.getelementptr(node.lhs)
        self.generatestore(where, self.typeget(node.lhs)[0], lhsptr, newvar)

    def llvmASTLoopForNode(self, node):
        self.Scopes.append(Scope(type=ScopeEnum.Loop, name='', dim=self.Scopes[-1].dim, tempvar=self.Scopes[-1].tempvar))
        self.NameSpace.append(Scope(type=ScopeEnum.Loop, name='', dim=self.Scopes[-1].dim, tempvar=0))
        self.Scopes[-1].dim = self.Scopes[-2].dim
        self.Scopes[-1].tempvar = self.Scopes[-2].tempvar
        self.llvm(node.initExpr)
        root = self.llvmfunc[self.getfuncname()][2]
        forcondind = len(root)
        forcond = f'for.cond.{len(root)}'
        root.append([f'for.cond.{len(root)}:\n'])
        forbodyind = len(root)
        forbody = f'for.body.{len(root)}'
        root.append([f'for.body.{len(root)}:\n'])
        forincind = len(root)
        forinc = f'for.inc.{len(root)}'
        root.append([f'for.inc.{len(root)}:\n'])
        forendind = len(root)
        forend = f'for.end.{len(root)}'
        root.append([f'for.end.{len(root)}:\n'])
        self.generatejump(root[self.Scopes[-1].dim], forcond)
        self.Scopes[-1].dim = forcondind
        self.generateloopcondition(root[self.Scopes[-1].dim], node.endCondition, forbody, forend)
        self.Scopes[-1].dim = forbodyind
        self.generateloopbody(root[self.Scopes[-1].dim], node.Smt, forinc)
        self.Scopes[-1].dim = forincind
        self.generateloopinc(root[self.Scopes[-1].dim], node.step, forcond)
        self.Scopes[-1].dim = forendind
        self.Scopes[-2].dim = self.Scopes[-1].dim
        self.Scopes[-2].tempvar = self.Scopes[-1].tempvar
        self.Scopes.pop()
        self.NameSpace.pop()

    def llvmASTLoopWhileNode(self, node):
        root = self.llvmfunc[self.getfuncname()][2]
        if type(node.Condition).__name__ == "ASTConstExprContextNode":
            if node.Condition.value:
                bodySmtind = len(root)
                bodySmt = f"whilebodySmt.{len(root)}"
                root.append([f'whilebodySmt.{len(root)}:\n'])
                endSmtind = len(root)
                endSmt = f"whileendSmt.{len(root)}"
                root.append([f'whileendSmt.{len(root)}:\n'])
                self.generatejump(root[self.Scopes[-1].dim], bodySmt)
                self.Scopes.append(Scope(type=ScopeEnum.Loop, name='', dim=self.Scopes[-1].dim, tempvar=self.Scopes[-1].tempvar))
                self.NameSpace.append(Scope(type=ScopeEnum.Loop, name='', dim=self.Scopes[-1].dim, tempvar=0))
                self.Scopes[-1].dim = bodySmtind
                self.Scopes[-1].tempvar = self.Scopes[-2].tempvar
                if type(node.Smt).__name__ == "ASTBlockSmtNode":
                    for smt in node.Smt.Smt:
                        self.llvm(smt)
                else:
                    self.llvm(node.Smt)
                self.generatejump(root[self.Scopes[-1].dim], bodySmt)
        else:
            condSmtind = len(root)
            condSmt = f"whilecondSmt.{len(root)}"
            root.append([f'whilecondSmt.{len(root)}:\n'])
            bodySmtind = len(root)
            bodySmt = f"whilebodySmt.{len(root)}"
            root.append([f'whilebodySmt.{len(root)}:\n'])
            endSmtind = len(root)
            endSmt = f"whileendSmt.{len(root)}"
            root.append([f'whileendSmt.{len(root)}:\n'])
            self.generatejump(root[self.Scopes[-1].dim], condSmt)
            self.Scopes.append(Scope(type=ScopeEnum.Loop, name='', dim=self.Scopes[-1].dim, tempvar=self.Scopes[-1].tempvar))
            self.NameSpace.append(Scope(type=ScopeEnum.Loop, name='', dim=self.Scopes[-1].dim, tempvar=0))
            self.Scopes[-1].dim = condSmtind
            self.Scopes[-1].tempvar = self.Scopes[-2].tempvar
            newvar = f"%._{self.Scopes[-1].tempvar}"
            self.Scopes[-1].tempvar += 1
            self.generateload(root[self.Scopes[-1].dim], typeclass(t=typeEnum.BOOL), node.Condition, newvar)
            self.generatebranch(root[self.Scopes[-1].dim], newvar, bodySmt, endSmt)
            self.Scopes[-1].dim = bodySmtind
            if type(node.Smt).__name__ == "ASTBlockSmtNode":
                for smt in node.Smt.Smt:
                    self.llvm(smt)
            else:
                self.llvm(node.Smt)
            self.generatejump(root[self.Scopes[-1].dim], condSmt)
            self.Scopes[-2].dim = endSmtind
            self.Scopes[-2].tempvar = self.Scopes[-1].tempvar
            self.Scopes.pop()
            self.NameSpace.pop()

    def generatejump(self, where, label):
        where.append(f'br label %{label}\n')

    def generateloopcondition(self, where, conditionnode, bodylabel, endlabel):
        newvar = f"%._{self.Scopes[-1].tempvar}"
        self.Scopes[-1].tempvar += 1
        self.generateload(where, typeclass(t=typeEnum.BOOL), conditionnode, newvar)
        self.generatebranch(where, newvar, bodylabel, endlabel)

    def generateloopbody(self, where, smtnode, tolabel):
        for smt in smtnode.Smt:
            self.llvm(smt)
        self.generatejump(self.llvmfunc[self.getfuncname()][2][self.Scopes[-1].dim], tolabel)

    def generateloopinc(self, where, stepnode, tolabel):
        self.llvm(stepnode)
        self.generatejump(where, tolabel)

    def generatebranch(self, where, var, label1, label2):
        where.append(f"br i1 {var}, label %{label1}, label %{label2}\n")

    def generateload(self, where, typetodo, vars, target):
        if type(vars).__name__ == 'ASTIdentifierExprNode':
            where.append(f"{target} = load {self.llvmtypeclass(typetodo)}, ptr {self.getname(vars.id)}\n")
        elif type(vars).__name__ == 'str':
            where.append(f"{target} = load {self.llvmtypeclass(typetodo)}, ptr {vars}\n")
        elif type(vars).__name__ == "ASTMemberVarExprNode":
            if type(vars.body).__name__ != "ASTIdentifierExprNode":
                newvar = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.NameSpace[-1].VarsBank[newvar] = newvar
                self.Scopes[-1].VarsBank[newvar] = self.typeget(vars.body)[0]
                self.generateload(where, self.typeget(vars.body)[0], vars.body, newvar)
                newvar = self.generategetelementptr(where, self.Scopes[-1].VarsBank[newvar], newvar, vars.id)
                self.generateload(where, self.gettype(newvar), newvar, target)
            else:
                newvar = self.generategetelementptr(where, self.typeget(vars.body)[0], self.getname(vars.body.id), vars.id)
                self.generateload(where, self.gettype(newvar), newvar, target)
        elif type(vars).__name__ == "ASTBinaryExprNode":
            if typetodo.dim > 0:
                raise Exception("TODO")
            elif typetodo.type == typeEnum.INT:
                if type(vars.lhs).__name__ == "ASTConstExprContextNode":
                    lhsnewvar = str(vars.lhs.value)
                else:
                    lhsnewvar = f"%._{self.Scopes[-1].tempvar}"
                    self.Scopes[-1].tempvar += 1
                    self.NameSpace[-1].VarsBank[lhsnewvar] = lhsnewvar
                    self.Scopes[-1].VarsBank[lhsnewvar] = typetodo
                    self.generateload(where, typetodo, vars.lhs, lhsnewvar)
                if type(vars.rhs).__name__ == "ASTConstExprContextNode":
                    rhsnewvar = str(vars.rhs.value)
                else:
                    rhsnewvar = f"%._{self.Scopes[-1].tempvar}"
                    self.Scopes[-1].tempvar += 1
                    self.NameSpace[-1].VarsBank[rhsnewvar] = rhsnewvar
                    self.Scopes[-1].VarsBank[rhsnewvar] = typetodo
                    self.generateload(where, typetodo, vars.rhs, rhsnewvar)
                self.generateFuncCall(where, None, vars.op, [lhsnewvar, rhsnewvar], target)
            elif typetodo.type == typeEnum.BOOL:
                if type(vars.lhs).__name__ == "ASTConstExprContextNode":
                    lhsnewvar = str(vars.lhs.value)
                else:
                    lhsnewvar = f"%._{self.Scopes[-1].tempvar}"
                    self.Scopes[-1].tempvar += 1
                    self.NameSpace[-1].VarsBank[lhsnewvar] = lhsnewvar
                    self.Scopes[-1].VarsBank[lhsnewvar] = typetodo
                    self.generateload(where, self.typeget(vars.lhs)[0], vars.lhs, lhsnewvar)
                if type(vars.rhs).__name__ == "ASTConstExprContextNode":
                    rhsnewvar = str(vars.rhs.value)
                else:
                    rhsnewvar = f"%._{self.Scopes[-1].tempvar}"
                    self.Scopes[-1].tempvar += 1
                    self.NameSpace[-1].VarsBank[rhsnewvar] = rhsnewvar
                    self.Scopes[-1].VarsBank[rhsnewvar] = typetodo
                    self.generateload(where, self.typeget(vars.rhs)[0], vars.rhs, rhsnewvar)
                lhstype = self.typeget(vars.lhs)[0]
                rhstype = self.typeget(vars.rhs)[0]
                if lhstype.dim > 0 or rhstype.dim > 0:
                    raise Exception("TODO")
                elif (lhstype.type == typeEnum.INT) and (rhstype.type == typeEnum.INT):
                    self.generateFuncCall(where, None, vars.op, ['i32', lhsnewvar, rhsnewvar], target)
                else:
                    raise Exception("TODO")
            else:
                raise Exception("TODO")
        elif type(vars).__name__ == "ASTUnaryExprNode":
            if vars.op == '+':
                self.generateload(where, typetodo, vars.body, target)
            elif vars.op == '-':
                newvar = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.generateload(where, typetodo, vars.body, newvar)
                self.generateFuncCall(where, None, '-', ['0', newvar], target)
            elif vars.op == '~':
                newvar = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.generateload(where, typetodo, vars.body, newvar)
                self.generateFuncCall(where, None, '^', [newvar, '-1'], target)
            elif vars.op == '!':
                newvar = f"%._{self.Scopes[-1].tempvar}"
                self.Scopes[-1].tempvar += 1
                self.generateload(where, typetodo, vars.body, newvar)
                self.generateFuncCall(where, None, '!', [newvar, 'true'], target)
        elif type(vars).__name__ == "ASTPrefixUpdateExprNode":
            bodyptr = self.getelementptr(vars.body)
            newvar = f"%._{self.Scopes[-1].tempvar}"
            self.Scopes[-1].tempvar += 1
            self.generateload(where, typeclass(t=typeEnum.INT), bodyptr, newvar)
            if vars.op == '++':
                self.generateFuncCall(where, None, '+', [newvar, '1'], target)
            else:
                self.generateFuncCall(where, None, '-', [newvar, '1'], target)
            self.generatestore(where, typeclass(t=typeEnum.INT), bodyptr, target)
        elif type(vars).__name__ == "ASTPostfixUpdateExprNode":
            bodyptr = self.getelementptr(vars.body)
            newvar = f"%._{self.Scopes[-1].tempvar}"
            self.Scopes[-1].tempvar += 1
            self.generateload(where, typeclass(t=typeEnum.INT), bodyptr, target)
            if vars.op == '++':
                self.generateFuncCall(where, None, '+', [target, '1'], newvar)
            else:
                self.generateFuncCall(where, None, '-', [target, '1'], newvar)
            self.generatestore(where, typeclass(t=typeEnum.INT), bodyptr, newvar)
        else:
            raise Exception("TODO")

    def generategetelementptr(self, where, typetodo, target, id):
        if typetodo.dim > 0:
            pass
        elif typetodo.type == typeEnum.CLASS:
            newvar = f"%._{self.Scopes[-1].tempvar}"
            self.Scopes[-1].tempvar += 1
            where.append(f"{newvar} = getelementptr %.CLASS.{typetodo.name}, ptr {target}, i32 {self.llvmclass[typetodo.name].index(id)}\n")
            self.Scopes[-1].VarsBank[newvar] = self.ClassBank[typetodo.name].ClassMember[id].type
            self.NameSpace[-1].VarsBank[newvar] = newvar
            return newvar

    def generatestore(self, where, typetodo, target, value):
        if type(value).__name__ == 'ASTIdentifierExprNode':
            newvar = f"._{len(where)}"
            self.NameSpace[-1].VarsBank[newvar] = newvar
            self.generateload(where, typetodo, value, newvar)
            where.append(f"store {self.llvmtypeclass(typetodo)} {newvar}, ptr {self.getname(target)}\n")
        elif type(value).__name__ == 'ASTNewClassNode':
            newvar = f"%.{len(where)}"
            self.NameSpace[-1].VarsBank[newvar] = newvar
            self.generateFuncCall(where, typeclass(typeEnum.CLASS), '__malloc', [f'sizeof(%.CLASS.{typetodo.name})'], newvar)
            where.append(f"store {self.llvmtypeclass(typetodo)} {newvar}, ptr {self.getname(target)}\n")
        elif type(value).__name__ == 'str':
            where.append(f"store {self.llvmtypeclass(typetodo)} {value}, ptr {self.getname(target)}\n")
        elif type(value).__name__ == "ASTConstExprContextNode":
            if value.type.type in [typeEnum.INT, typeEnum.BOOL]:
                where.append(f"store {self.llvmtypeclass(typetodo)} {value.value}, ptr {self.getname(target)}\n")
            elif value.type.type == typeEnum.STRING:
                where.append(f"store ptr @.str.{self.globalstring.index(value.value)}, ptr {self.getname(target)}\n")
            elif value.type.type == typeEnum.NULL:
                where.append(f"store ptr null, ptr {self.getname(target)}\n")
        else:
            raise Exception("TODO")

    def generateFuncCall(self, where, retType, funcname, arglist, retwhere):
        if funcname in self.symbol:
            where.append(f"{retwhere} = {self.symbol[funcname]} i32 {arglist[0]}, {arglist[1]}\n")
        elif funcname in self.logic:
            where.append(f"{retwhere} = icmp {self.logic[funcname]} {arglist[0]} {arglist[1]}, {arglist[2]}\n")
        elif funcname == '!':
            where.append(f"{retwhere} = xor i1 {arglist[0]}, {arglist[1]}\n")
        elif retType == typeclass(t=typeEnum.VOID):
            res = f"call void @{funcname}("
            for i in range(len(arglist)):
                if i != 0:
                    res = res + ', '
                res = res + self.llvmfunc[funcname][1][i][0] + ' ' + arglist[i]
            res = res + ')\n'
            where.append(res)
        elif retType.type == typeEnum.CLASS:
            res = f"{retwhere} = call ptr @{funcname}("
            for i in range(len(arglist)):
                if i != 0:
                    res = res + ', '
                res = res + self.llvmfunc[funcname][1][i][0] + ' ' + arglist[i]
            res = res + ')\n'
            where.append(res)
        else:
            raise Exception("TODO")

    def generateret(self, where, typetodo, retNode):
        if typetodo == typeclass(t=typeEnum.VOID):
            where.append(f"ret void\n")
        else:
            where.append(f"ret {self.llvmtypeclass(typetodo)} {retNode}\n")

    def generatealloca(self, where, typetodo, target):
        if typetodo.dim > 0:
            pass
        elif typetodo.type == typeEnum.CLASS:
            where.append(f"{target} = alloca ptr\n")
        elif typetodo.type == typeEnum.INT:
            where.append(f"{target} = alloca i32\n")
        elif typetodo.type == typeEnum.STRING:
            where.append(f"{target} = alloca ptr\n")
        else:
            raise Exception("TODO")

    def getname(self, name):
        for i in range(len(self.NameSpace) - 1, -1, -1):
            if name in self.NameSpace[i].VarsBank:
                return self.NameSpace[i].VarsBank[name]

    def gettype(self, name):
        for i in range(len(self.Scopes) - 1, -1, -1):
            if name in self.Scopes[i].VarsBank:
                return self.Scopes[i].VarsBank[name]


if __name__ == "__main__":
    # root = os.listdir(sys.argv[1])
    # for files in root:
    #     if files[-3:] == '.mx':
    #         try:
    #             print(files + ':', end='')
    #             input_stream = FileStream(sys.argv[1] + '\\' + files, encoding="utf-8")
    #             lexer = helloLexer(input_stream)
    #             lexer._listeners = [MyErrorListener()]
    #             stream = CommonTokenStream(lexer)
    #             parser = helloParser(stream)
    #             parser._listeners = [MyErrorListener()]
    #             cst = parser.body()
    #             builder = ASTBuilder()
    #             ast = builder.build(cst)
    #             flag = builder.check(ast)
    #         except Exception as e:
    #             flag = False
    #
    #         f5 = open(sys.argv[1] + '\\' + files, encoding="utf-8")
    #         content = f5.readlines()
    #         f5.close()
    #         print(('Verdict: Success\n' in content) == flag)
    #     elif files[-3:] == 'txt':
    #         continue
    #     else:
    #         subfile = os.listdir(sys.argv[1] + '\\' + files)
    #         for file in subfile:
    #             try:
    #                 print(files + '\\' + file + ':', end='')
    #                 input_stream = FileStream(sys.argv[1] + '\\' + files + '\\' + file, encoding="utf-8")
    #                 lexer = helloLexer(input_stream)
    #                 lexer._listeners = [MyErrorListener()]
    #                 stream = CommonTokenStream(lexer)
    #                 parser = helloParser(stream)
    #                 parser._listeners = [MyErrorListener()]
    #                 cst = parser.body()
    #                 builder = ASTBuilder()
    #                 ast = builder.build(cst)
    #                 flag = builder.check(ast)
    #             except Exception as e:
    #                 flag = False
    #
    #             f5 = open(sys.argv[1] + '\\' + files + '\\' + file, encoding="utf-8")
    #             content = f5.readlines()
    #             f5.close()
    #             print(('Verdict: Success\n' in content) == flag)

    # sys.stdin = codecs.getreader('utf-8')(sys.stdin)
    # input_stream = StdinStream()

    input_stream = FileStream(r"C:\Users\14908\Desktop\PPCA\Complier\test.txt", encoding="utf-8")
    lexer = helloLexer(input_stream)
    lexer._listeners = [MyErrorListener()]
    stream = CommonTokenStream(lexer)
    parser = helloParser(stream)
    parser._listeners = [MyErrorListener()]
    cst = parser.body()
    builder = ASTBuilder()
    ast = builder.build(cst)
    flag = builder.check(ast)
    print(flag)
    builder.llvm(ast)
    output.close()

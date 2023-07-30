# Generated from C:/Users/14908/Desktop/PPCA/Complier\hello.g4 by ANTLR 4.12.0
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .helloParser import helloParser
else:
    from helloParser import helloParser

# This class defines a complete listener for a parse tree produced by helloParser.
class helloListener(ParseTreeListener):

    # Enter a parse tree produced by helloParser#body.
    def enterBody(self, ctx:helloParser.BodyContext):
        pass

    # Exit a parse tree produced by helloParser#body.
    def exitBody(self, ctx:helloParser.BodyContext):
        pass


    # Enter a parse tree produced by helloParser#VarDeclar.
    def enterVarDeclar(self, ctx:helloParser.VarDeclarContext):
        pass

    # Exit a parse tree produced by helloParser#VarDeclar.
    def exitVarDeclar(self, ctx:helloParser.VarDeclarContext):
        pass


    # Enter a parse tree produced by helloParser#ClassDeclar.
    def enterClassDeclar(self, ctx:helloParser.ClassDeclarContext):
        pass

    # Exit a parse tree produced by helloParser#ClassDeclar.
    def exitClassDeclar(self, ctx:helloParser.ClassDeclarContext):
        pass


    # Enter a parse tree produced by helloParser#FuncDeclar.
    def enterFuncDeclar(self, ctx:helloParser.FuncDeclarContext):
        pass

    # Exit a parse tree produced by helloParser#FuncDeclar.
    def exitFuncDeclar(self, ctx:helloParser.FuncDeclarContext):
        pass


    # Enter a parse tree produced by helloParser#variabledeclaration.
    def enterVariabledeclaration(self, ctx:helloParser.VariabledeclarationContext):
        pass

    # Exit a parse tree produced by helloParser#variabledeclaration.
    def exitVariabledeclaration(self, ctx:helloParser.VariabledeclarationContext):
        pass


    # Enter a parse tree produced by helloParser#ArrayCase.
    def enterArrayCase(self, ctx:helloParser.ArrayCaseContext):
        pass

    # Exit a parse tree produced by helloParser#ArrayCase.
    def exitArrayCase(self, ctx:helloParser.ArrayCaseContext):
        pass


    # Enter a parse tree produced by helloParser#PrimeCase.
    def enterPrimeCase(self, ctx:helloParser.PrimeCaseContext):
        pass

    # Exit a parse tree produced by helloParser#PrimeCase.
    def exitPrimeCase(self, ctx:helloParser.PrimeCaseContext):
        pass


    # Enter a parse tree produced by helloParser#ClassCase.
    def enterClassCase(self, ctx:helloParser.ClassCaseContext):
        pass

    # Exit a parse tree produced by helloParser#ClassCase.
    def exitClassCase(self, ctx:helloParser.ClassCaseContext):
        pass


    # Enter a parse tree produced by helloParser#easytype.
    def enterEasytype(self, ctx:helloParser.EasytypeContext):
        pass

    # Exit a parse tree produced by helloParser#easytype.
    def exitEasytype(self, ctx:helloParser.EasytypeContext):
        pass


    # Enter a parse tree produced by helloParser#initialize.
    def enterInitialize(self, ctx:helloParser.InitializeContext):
        pass

    # Exit a parse tree produced by helloParser#initialize.
    def exitInitialize(self, ctx:helloParser.InitializeContext):
        pass


    # Enter a parse tree produced by helloParser#ConstExpr.
    def enterConstExpr(self, ctx:helloParser.ConstExprContext):
        pass

    # Exit a parse tree produced by helloParser#ConstExpr.
    def exitConstExpr(self, ctx:helloParser.ConstExprContext):
        pass


    # Enter a parse tree produced by helloParser#PostfixUpdateExpr.
    def enterPostfixUpdateExpr(self, ctx:helloParser.PostfixUpdateExprContext):
        pass

    # Exit a parse tree produced by helloParser#PostfixUpdateExpr.
    def exitPostfixUpdateExpr(self, ctx:helloParser.PostfixUpdateExprContext):
        pass


    # Enter a parse tree produced by helloParser#BinaryExpr.
    def enterBinaryExpr(self, ctx:helloParser.BinaryExprContext):
        pass

    # Exit a parse tree produced by helloParser#BinaryExpr.
    def exitBinaryExpr(self, ctx:helloParser.BinaryExprContext):
        pass


    # Enter a parse tree produced by helloParser#NewExpr.
    def enterNewExpr(self, ctx:helloParser.NewExprContext):
        pass

    # Exit a parse tree produced by helloParser#NewExpr.
    def exitNewExpr(self, ctx:helloParser.NewExprContext):
        pass


    # Enter a parse tree produced by helloParser#PrefixUpdateExpr.
    def enterPrefixUpdateExpr(self, ctx:helloParser.PrefixUpdateExprContext):
        pass

    # Exit a parse tree produced by helloParser#PrefixUpdateExpr.
    def exitPrefixUpdateExpr(self, ctx:helloParser.PrefixUpdateExprContext):
        pass


    # Enter a parse tree produced by helloParser#LhsExpr.
    def enterLhsExpr(self, ctx:helloParser.LhsExprContext):
        pass

    # Exit a parse tree produced by helloParser#LhsExpr.
    def exitLhsExpr(self, ctx:helloParser.LhsExprContext):
        pass


    # Enter a parse tree produced by helloParser#ExpExpr.
    def enterExpExpr(self, ctx:helloParser.ExpExprContext):
        pass

    # Exit a parse tree produced by helloParser#ExpExpr.
    def exitExpExpr(self, ctx:helloParser.ExpExprContext):
        pass


    # Enter a parse tree produced by helloParser#TriExpr.
    def enterTriExpr(self, ctx:helloParser.TriExprContext):
        pass

    # Exit a parse tree produced by helloParser#TriExpr.
    def exitTriExpr(self, ctx:helloParser.TriExprContext):
        pass


    # Enter a parse tree produced by helloParser#UnaryExpr.
    def enterUnaryExpr(self, ctx:helloParser.UnaryExprContext):
        pass

    # Exit a parse tree produced by helloParser#UnaryExpr.
    def exitUnaryExpr(self, ctx:helloParser.UnaryExprContext):
        pass


    # Enter a parse tree produced by helloParser#AssignExpr.
    def enterAssignExpr(self, ctx:helloParser.AssignExprContext):
        pass

    # Exit a parse tree produced by helloParser#AssignExpr.
    def exitAssignExpr(self, ctx:helloParser.AssignExprContext):
        pass


    # Enter a parse tree produced by helloParser#newexpression.
    def enterNewexpression(self, ctx:helloParser.NewexpressionContext):
        pass

    # Exit a parse tree produced by helloParser#newexpression.
    def exitNewexpression(self, ctx:helloParser.NewexpressionContext):
        pass


    # Enter a parse tree produced by helloParser#NewClass.
    def enterNewClass(self, ctx:helloParser.NewClassContext):
        pass

    # Exit a parse tree produced by helloParser#NewClass.
    def exitNewClass(self, ctx:helloParser.NewClassContext):
        pass


    # Enter a parse tree produced by helloParser#NewClassArray.
    def enterNewClassArray(self, ctx:helloParser.NewClassArrayContext):
        pass

    # Exit a parse tree produced by helloParser#NewClassArray.
    def exitNewClassArray(self, ctx:helloParser.NewClassArrayContext):
        pass


    # Enter a parse tree produced by helloParser#NewPrimeArray.
    def enterNewPrimeArray(self, ctx:helloParser.NewPrimeArrayContext):
        pass

    # Exit a parse tree produced by helloParser#NewPrimeArray.
    def exitNewPrimeArray(self, ctx:helloParser.NewPrimeArrayContext):
        pass


    # Enter a parse tree produced by helloParser#bracketwithargs.
    def enterBracketwithargs(self, ctx:helloParser.BracketwithargsContext):
        pass

    # Exit a parse tree produced by helloParser#bracketwithargs.
    def exitBracketwithargs(self, ctx:helloParser.BracketwithargsContext):
        pass


    # Enter a parse tree produced by helloParser#bracketwithoutargs.
    def enterBracketwithoutargs(self, ctx:helloParser.BracketwithoutargsContext):
        pass

    # Exit a parse tree produced by helloParser#bracketwithoutargs.
    def exitBracketwithoutargs(self, ctx:helloParser.BracketwithoutargsContext):
        pass


    # Enter a parse tree produced by helloParser#Numconstexpression.
    def enterNumconstexpression(self, ctx:helloParser.NumconstexpressionContext):
        pass

    # Exit a parse tree produced by helloParser#Numconstexpression.
    def exitNumconstexpression(self, ctx:helloParser.NumconstexpressionContext):
        pass


    # Enter a parse tree produced by helloParser#Stringconstexpression.
    def enterStringconstexpression(self, ctx:helloParser.StringconstexpressionContext):
        pass

    # Exit a parse tree produced by helloParser#Stringconstexpression.
    def exitStringconstexpression(self, ctx:helloParser.StringconstexpressionContext):
        pass


    # Enter a parse tree produced by helloParser#Boolconstexpression.
    def enterBoolconstexpression(self, ctx:helloParser.BoolconstexpressionContext):
        pass

    # Exit a parse tree produced by helloParser#Boolconstexpression.
    def exitBoolconstexpression(self, ctx:helloParser.BoolconstexpressionContext):
        pass


    # Enter a parse tree produced by helloParser#Nullconstexpression.
    def enterNullconstexpression(self, ctx:helloParser.NullconstexpressionContext):
        pass

    # Exit a parse tree produced by helloParser#Nullconstexpression.
    def exitNullconstexpression(self, ctx:helloParser.NullconstexpressionContext):
        pass


    # Enter a parse tree produced by helloParser#ArrayExpr.
    def enterArrayExpr(self, ctx:helloParser.ArrayExprContext):
        pass

    # Exit a parse tree produced by helloParser#ArrayExpr.
    def exitArrayExpr(self, ctx:helloParser.ArrayExprContext):
        pass


    # Enter a parse tree produced by helloParser#IdentifierExpr.
    def enterIdentifierExpr(self, ctx:helloParser.IdentifierExprContext):
        pass

    # Exit a parse tree produced by helloParser#IdentifierExpr.
    def exitIdentifierExpr(self, ctx:helloParser.IdentifierExprContext):
        pass


    # Enter a parse tree produced by helloParser#MemberVarExpr.
    def enterMemberVarExpr(self, ctx:helloParser.MemberVarExprContext):
        pass

    # Exit a parse tree produced by helloParser#MemberVarExpr.
    def exitMemberVarExpr(self, ctx:helloParser.MemberVarExprContext):
        pass


    # Enter a parse tree produced by helloParser#MemberFuncExpr.
    def enterMemberFuncExpr(self, ctx:helloParser.MemberFuncExprContext):
        pass

    # Exit a parse tree produced by helloParser#MemberFuncExpr.
    def exitMemberFuncExpr(self, ctx:helloParser.MemberFuncExprContext):
        pass


    # Enter a parse tree produced by helloParser#ThisExpr.
    def enterThisExpr(self, ctx:helloParser.ThisExprContext):
        pass

    # Exit a parse tree produced by helloParser#ThisExpr.
    def exitThisExpr(self, ctx:helloParser.ThisExprContext):
        pass


    # Enter a parse tree produced by helloParser#ParaExpr.
    def enterParaExpr(self, ctx:helloParser.ParaExprContext):
        pass

    # Exit a parse tree produced by helloParser#ParaExpr.
    def exitParaExpr(self, ctx:helloParser.ParaExprContext):
        pass


    # Enter a parse tree produced by helloParser#FuncCallExpr.
    def enterFuncCallExpr(self, ctx:helloParser.FuncCallExprContext):
        pass

    # Exit a parse tree produced by helloParser#FuncCallExpr.
    def exitFuncCallExpr(self, ctx:helloParser.FuncCallExprContext):
        pass


    # Enter a parse tree produced by helloParser#funcarglist.
    def enterFuncarglist(self, ctx:helloParser.FuncarglistContext):
        pass

    # Exit a parse tree produced by helloParser#funcarglist.
    def exitFuncarglist(self, ctx:helloParser.FuncarglistContext):
        pass


    # Enter a parse tree produced by helloParser#classdeclaration.
    def enterClassdeclaration(self, ctx:helloParser.ClassdeclarationContext):
        pass

    # Exit a parse tree produced by helloParser#classdeclaration.
    def exitClassdeclaration(self, ctx:helloParser.ClassdeclarationContext):
        pass


    # Enter a parse tree produced by helloParser#ClassMemberDeclar.
    def enterClassMemberDeclar(self, ctx:helloParser.ClassMemberDeclarContext):
        pass

    # Exit a parse tree produced by helloParser#ClassMemberDeclar.
    def exitClassMemberDeclar(self, ctx:helloParser.ClassMemberDeclarContext):
        pass


    # Enter a parse tree produced by helloParser#ClassMemberFuncDeclar.
    def enterClassMemberFuncDeclar(self, ctx:helloParser.ClassMemberFuncDeclarContext):
        pass

    # Exit a parse tree produced by helloParser#ClassMemberFuncDeclar.
    def exitClassMemberFuncDeclar(self, ctx:helloParser.ClassMemberFuncDeclarContext):
        pass


    # Enter a parse tree produced by helloParser#ClassConstructorDeclar.
    def enterClassConstructorDeclar(self, ctx:helloParser.ClassConstructorDeclarContext):
        pass

    # Exit a parse tree produced by helloParser#ClassConstructorDeclar.
    def exitClassConstructorDeclar(self, ctx:helloParser.ClassConstructorDeclarContext):
        pass


    # Enter a parse tree produced by helloParser#classConstructFunc.
    def enterClassConstructFunc(self, ctx:helloParser.ClassConstructFuncContext):
        pass

    # Exit a parse tree produced by helloParser#classConstructFunc.
    def exitClassConstructFunc(self, ctx:helloParser.ClassConstructFuncContext):
        pass


    # Enter a parse tree produced by helloParser#blockStatement.
    def enterBlockStatement(self, ctx:helloParser.BlockStatementContext):
        pass

    # Exit a parse tree produced by helloParser#blockStatement.
    def exitBlockStatement(self, ctx:helloParser.BlockStatementContext):
        pass


    # Enter a parse tree produced by helloParser#functiondeclaration.
    def enterFunctiondeclaration(self, ctx:helloParser.FunctiondeclarationContext):
        pass

    # Exit a parse tree produced by helloParser#functiondeclaration.
    def exitFunctiondeclaration(self, ctx:helloParser.FunctiondeclarationContext):
        pass


    # Enter a parse tree produced by helloParser#funcarglistDec.
    def enterFuncarglistDec(self, ctx:helloParser.FuncarglistDecContext):
        pass

    # Exit a parse tree produced by helloParser#funcarglistDec.
    def exitFuncarglistDec(self, ctx:helloParser.FuncarglistDecContext):
        pass


    # Enter a parse tree produced by helloParser#funcparam.
    def enterFuncparam(self, ctx:helloParser.FuncparamContext):
        pass

    # Exit a parse tree produced by helloParser#funcparam.
    def exitFuncparam(self, ctx:helloParser.FuncparamContext):
        pass


    # Enter a parse tree produced by helloParser#BlockSmt.
    def enterBlockSmt(self, ctx:helloParser.BlockSmtContext):
        pass

    # Exit a parse tree produced by helloParser#BlockSmt.
    def exitBlockSmt(self, ctx:helloParser.BlockSmtContext):
        pass


    # Enter a parse tree produced by helloParser#VarDeclarSmt.
    def enterVarDeclarSmt(self, ctx:helloParser.VarDeclarSmtContext):
        pass

    # Exit a parse tree produced by helloParser#VarDeclarSmt.
    def exitVarDeclarSmt(self, ctx:helloParser.VarDeclarSmtContext):
        pass


    # Enter a parse tree produced by helloParser#ExprSmt.
    def enterExprSmt(self, ctx:helloParser.ExprSmtContext):
        pass

    # Exit a parse tree produced by helloParser#ExprSmt.
    def exitExprSmt(self, ctx:helloParser.ExprSmtContext):
        pass


    # Enter a parse tree produced by helloParser#BranchSmt.
    def enterBranchSmt(self, ctx:helloParser.BranchSmtContext):
        pass

    # Exit a parse tree produced by helloParser#BranchSmt.
    def exitBranchSmt(self, ctx:helloParser.BranchSmtContext):
        pass


    # Enter a parse tree produced by helloParser#LoopSmt.
    def enterLoopSmt(self, ctx:helloParser.LoopSmtContext):
        pass

    # Exit a parse tree produced by helloParser#LoopSmt.
    def exitLoopSmt(self, ctx:helloParser.LoopSmtContext):
        pass


    # Enter a parse tree produced by helloParser#ContinueSmt.
    def enterContinueSmt(self, ctx:helloParser.ContinueSmtContext):
        pass

    # Exit a parse tree produced by helloParser#ContinueSmt.
    def exitContinueSmt(self, ctx:helloParser.ContinueSmtContext):
        pass


    # Enter a parse tree produced by helloParser#BreakSmt.
    def enterBreakSmt(self, ctx:helloParser.BreakSmtContext):
        pass

    # Exit a parse tree produced by helloParser#BreakSmt.
    def exitBreakSmt(self, ctx:helloParser.BreakSmtContext):
        pass


    # Enter a parse tree produced by helloParser#ReturnSmt.
    def enterReturnSmt(self, ctx:helloParser.ReturnSmtContext):
        pass

    # Exit a parse tree produced by helloParser#ReturnSmt.
    def exitReturnSmt(self, ctx:helloParser.ReturnSmtContext):
        pass


    # Enter a parse tree produced by helloParser#EmptySmt.
    def enterEmptySmt(self, ctx:helloParser.EmptySmtContext):
        pass

    # Exit a parse tree produced by helloParser#EmptySmt.
    def exitEmptySmt(self, ctx:helloParser.EmptySmtContext):
        pass


    # Enter a parse tree produced by helloParser#branchStatement.
    def enterBranchStatement(self, ctx:helloParser.BranchStatementContext):
        pass

    # Exit a parse tree produced by helloParser#branchStatement.
    def exitBranchStatement(self, ctx:helloParser.BranchStatementContext):
        pass


    # Enter a parse tree produced by helloParser#WhileSmt.
    def enterWhileSmt(self, ctx:helloParser.WhileSmtContext):
        pass

    # Exit a parse tree produced by helloParser#WhileSmt.
    def exitWhileSmt(self, ctx:helloParser.WhileSmtContext):
        pass


    # Enter a parse tree produced by helloParser#DecForSmt.
    def enterDecForSmt(self, ctx:helloParser.DecForSmtContext):
        pass

    # Exit a parse tree produced by helloParser#DecForSmt.
    def exitDecForSmt(self, ctx:helloParser.DecForSmtContext):
        pass


    # Enter a parse tree produced by helloParser#ExpForSmt.
    def enterExpForSmt(self, ctx:helloParser.ExpForSmtContext):
        pass

    # Exit a parse tree produced by helloParser#ExpForSmt.
    def exitExpForSmt(self, ctx:helloParser.ExpForSmtContext):
        pass


    # Enter a parse tree produced by helloParser#emptyStatement.
    def enterEmptyStatement(self, ctx:helloParser.EmptyStatementContext):
        pass

    # Exit a parse tree produced by helloParser#emptyStatement.
    def exitEmptyStatement(self, ctx:helloParser.EmptyStatementContext):
        pass



del helloParser
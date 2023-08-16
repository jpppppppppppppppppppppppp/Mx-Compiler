# Generated from C:/Users/14908/Desktop/PPCA/Compiler\hello.g4 by ANTLR 4.12.0
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .helloParser import helloParser
else:
    from helloParser import helloParser

# This class defines a complete generic visitor for a parse tree produced by helloParser.

class helloVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by helloParser#body.
    def visitBody(self, ctx:helloParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#VarDeclar.
    def visitVarDeclar(self, ctx:helloParser.VarDeclarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#ClassDeclar.
    def visitClassDeclar(self, ctx:helloParser.ClassDeclarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#FuncDeclar.
    def visitFuncDeclar(self, ctx:helloParser.FuncDeclarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#variabledeclaration.
    def visitVariabledeclaration(self, ctx:helloParser.VariabledeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#ArrayCase.
    def visitArrayCase(self, ctx:helloParser.ArrayCaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#PrimeCase.
    def visitPrimeCase(self, ctx:helloParser.PrimeCaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#ClassCase.
    def visitClassCase(self, ctx:helloParser.ClassCaseContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#easytype.
    def visitEasytype(self, ctx:helloParser.EasytypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#initialize.
    def visitInitialize(self, ctx:helloParser.InitializeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#ConstExpr.
    def visitConstExpr(self, ctx:helloParser.ConstExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#PostfixUpdateExpr.
    def visitPostfixUpdateExpr(self, ctx:helloParser.PostfixUpdateExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#BinaryExpr.
    def visitBinaryExpr(self, ctx:helloParser.BinaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#NewExpr.
    def visitNewExpr(self, ctx:helloParser.NewExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#PrefixUpdateExpr.
    def visitPrefixUpdateExpr(self, ctx:helloParser.PrefixUpdateExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#LhsExpr.
    def visitLhsExpr(self, ctx:helloParser.LhsExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#ExpExpr.
    def visitExpExpr(self, ctx:helloParser.ExpExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#TriExpr.
    def visitTriExpr(self, ctx:helloParser.TriExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#UnaryExpr.
    def visitUnaryExpr(self, ctx:helloParser.UnaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#AssignExpr.
    def visitAssignExpr(self, ctx:helloParser.AssignExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#newexpression.
    def visitNewexpression(self, ctx:helloParser.NewexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#NewClass.
    def visitNewClass(self, ctx:helloParser.NewClassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#NewClassArray.
    def visitNewClassArray(self, ctx:helloParser.NewClassArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#NewPrimeArray.
    def visitNewPrimeArray(self, ctx:helloParser.NewPrimeArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#bracketwithargs.
    def visitBracketwithargs(self, ctx:helloParser.BracketwithargsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#bracketwithoutargs.
    def visitBracketwithoutargs(self, ctx:helloParser.BracketwithoutargsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#Numconstexpression.
    def visitNumconstexpression(self, ctx:helloParser.NumconstexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#Stringconstexpression.
    def visitStringconstexpression(self, ctx:helloParser.StringconstexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#Boolconstexpression.
    def visitBoolconstexpression(self, ctx:helloParser.BoolconstexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#Nullconstexpression.
    def visitNullconstexpression(self, ctx:helloParser.NullconstexpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#ArrayExpr.
    def visitArrayExpr(self, ctx:helloParser.ArrayExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#IdentifierExpr.
    def visitIdentifierExpr(self, ctx:helloParser.IdentifierExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#MemberVarExpr.
    def visitMemberVarExpr(self, ctx:helloParser.MemberVarExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#MemberFuncExpr.
    def visitMemberFuncExpr(self, ctx:helloParser.MemberFuncExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#ThisExpr.
    def visitThisExpr(self, ctx:helloParser.ThisExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#ParaExpr.
    def visitParaExpr(self, ctx:helloParser.ParaExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#FuncCallExpr.
    def visitFuncCallExpr(self, ctx:helloParser.FuncCallExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#funcarglist.
    def visitFuncarglist(self, ctx:helloParser.FuncarglistContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#classdeclaration.
    def visitClassdeclaration(self, ctx:helloParser.ClassdeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#ClassMemberDeclar.
    def visitClassMemberDeclar(self, ctx:helloParser.ClassMemberDeclarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#ClassMemberFuncDeclar.
    def visitClassMemberFuncDeclar(self, ctx:helloParser.ClassMemberFuncDeclarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#ClassConstructorDeclar.
    def visitClassConstructorDeclar(self, ctx:helloParser.ClassConstructorDeclarContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#classConstructFunc.
    def visitClassConstructFunc(self, ctx:helloParser.ClassConstructFuncContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#blockStatement.
    def visitBlockStatement(self, ctx:helloParser.BlockStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#functiondeclaration.
    def visitFunctiondeclaration(self, ctx:helloParser.FunctiondeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#funcarglistDec.
    def visitFuncarglistDec(self, ctx:helloParser.FuncarglistDecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#funcparam.
    def visitFuncparam(self, ctx:helloParser.FuncparamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#BlockSmt.
    def visitBlockSmt(self, ctx:helloParser.BlockSmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#VarDeclarSmt.
    def visitVarDeclarSmt(self, ctx:helloParser.VarDeclarSmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#ExprSmt.
    def visitExprSmt(self, ctx:helloParser.ExprSmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#BranchSmt.
    def visitBranchSmt(self, ctx:helloParser.BranchSmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#LoopSmt.
    def visitLoopSmt(self, ctx:helloParser.LoopSmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#ContinueSmt.
    def visitContinueSmt(self, ctx:helloParser.ContinueSmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#BreakSmt.
    def visitBreakSmt(self, ctx:helloParser.BreakSmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#ReturnSmt.
    def visitReturnSmt(self, ctx:helloParser.ReturnSmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#EmptySmt.
    def visitEmptySmt(self, ctx:helloParser.EmptySmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#branchStatement.
    def visitBranchStatement(self, ctx:helloParser.BranchStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#WhileSmt.
    def visitWhileSmt(self, ctx:helloParser.WhileSmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#DecForSmt.
    def visitDecForSmt(self, ctx:helloParser.DecForSmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#ExpForSmt.
    def visitExpForSmt(self, ctx:helloParser.ExpForSmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by helloParser#emptyStatement.
    def visitEmptyStatement(self, ctx:helloParser.EmptyStatementContext):
        return self.visitChildren(ctx)



del helloParser
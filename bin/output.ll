declare void @print(ptr)
declare void @println(ptr)
declare void @printInt(i32)
declare void @printlnInt(i32)
declare ptr @getString()
declare i32 @getInt()
declare ptr @toString(i32)
declare ptr @string.string()
declare i32 @string.length(ptr)
declare ptr @string.substring(ptr, i32, i32)
declare i32 @string.parseInt(ptr)
declare i32 @string.ord(ptr, i32)
declare ptr @string.add(ptr, ptr)
declare i1 @string.equal(ptr, ptr)
declare i1 @string.notEqual(ptr, ptr)
declare i1 @string.less(ptr, ptr)
declare i1 @string.lessOrEqual(ptr, ptr)
declare i1 @string.greater(ptr, ptr)
declare i1 @string.greaterOrEqual(ptr, ptr)
declare i32 @__array.size(ptr)
declare ptr @__newPtrArray(i32)
declare ptr @__newIntArray(i32)
declare ptr @__newBoolArray(i32)
declare ptr @malloc(i32)


@.true = global i32 1
@.false = global i32 1
@.string.0 = global [ 1 x i8 ] c"\00"
define i32 @qpow(i32 %.a, i32 %.p, i32 %.mod){
entry:
	%.return = alloca i32
	store i32 0, ptr %.return
	%.arg_a = alloca i32
	store i32 %.a, ptr %.arg_a
	%.arg_p = alloca i32
	store i32 %.p, ptr %.arg_p
	%.arg_mod = alloca i32
	store i32 %.mod, ptr %.arg_mod
	%.t.2.0 = alloca i32
	store i32 1, ptr %.t.2.0
	%.y.2.0 = alloca i32
	%._0 = load i32, ptr %.arg_a
	store i32 %._0, ptr %.y.2.0
	br label %whilecondSmt.2

return:
	%._23 = load i32, ptr %.return
	ret i32 %._23

whilecondSmt.2:
	%._2 = load i32, ptr %.arg_p
	%._3 = icmp sgt i32 %._2, 0
	%._1 = zext i1 %._3 to i32
	%._4 = trunc i32 %._1 to i1
	br i1 %._4, label %whilebodySmt.3, label %whileendSmt.4

whilebodySmt.3:
	%._7 = load i32, ptr %.arg_p
	%._6 = and i32 1, %._7
	%._8 = icmp eq i32 %._6, 1
	%._5 = zext i1 %._8 to i32
	%._9 = trunc i32 %._5 to i1
	br i1 %._9, label %ifSmt.5, label %ifendSmt.6

whileendSmt.4:
	%._22 = load i32, ptr %.t.2.0
	store i32 %._22, ptr %.return
	br label %return
	br label %return

ifSmt.5:
	%._12 = load i32, ptr %.t.2.0
	%._13 = load i32, ptr %.y.2.0
	%._11 = mul i32 %._12, %._13
	%._14 = load i32, ptr %.arg_mod
	%._10 = srem i32 %._11, %._14
	store i32 %._10, ptr %.t.2.0
	br label %ifendSmt.6

ifendSmt.6:
	%._17 = load i32, ptr %.y.2.0
	%._18 = load i32, ptr %.y.2.0
	%._16 = mul i32 %._17, %._18
	%._19 = load i32, ptr %.arg_mod
	%._15 = srem i32 %._16, %._19
	store i32 %._15, ptr %.y.2.0
	%._21 = load i32, ptr %.arg_p
	%._20 = sdiv i32 %._21, 2
	store i32 %._20, ptr %.arg_p
	br label %whilecondSmt.2

}
define i32 @main(){
entry:
	%.return = alloca i32
	store i32 0, ptr %.return
	%._1 =  call i32 @qpow( i32 2,i32 10,i32 10000 )
	%._0 =  call ptr @toString( i32 %._1 )
	call void @println( ptr %._0 )
	store i32 0, ptr %.return
	br label %return
	br label %return

return:
	%._2 = load i32, ptr %.return
	ret i32 %._2

}

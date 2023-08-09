; ModuleID = 'builtin.c'
source_filename = "builtin.c"
target datalayout = "e-m:e-p:32:32-i64:64-n32-S128"
target triple = "riscv32-unknown-unknown-elf"

@.str = private unnamed_addr constant [3 x i8] c"%s\00", align 1
@.str.1 = private unnamed_addr constant [4 x i8] c"%s\0A\00", align 1
@.str.2 = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str.3 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1

; Function Attrs: noinline nounwind optnone
define dso_local void @print(ptr noundef %0) #0 {
  %2 = alloca ptr, align 4
  store ptr %0, ptr %2, align 4
  %3 = load ptr, ptr %2, align 4
  %4 = call i32 (ptr, ...) @printf(ptr noundef @.str, ptr noundef %3) #2
  ret void
}

declare dso_local i32 @printf(ptr noundef, ...) #1

; Function Attrs: noinline nounwind optnone
define dso_local void @println(ptr noundef %0) #0 {
  %2 = alloca ptr, align 4
  store ptr %0, ptr %2, align 4
  %3 = load ptr, ptr %2, align 4
  %4 = call i32 (ptr, ...) @printf(ptr noundef @.str.1, ptr noundef %3) #2
  ret void
}

; Function Attrs: noinline nounwind optnone
define dso_local void @printInt(i32 noundef %0) #0 {
  %2 = alloca i32, align 4
  store i32 %0, ptr %2, align 4
  %3 = load i32, ptr %2, align 4
  %4 = call i32 (ptr, ...) @printf(ptr noundef @.str.2, i32 noundef %3) #2
  ret void
}

; Function Attrs: noinline nounwind optnone
define dso_local void @printlnInt(i32 noundef %0) #0 {
  %2 = alloca i32, align 4
  store i32 %0, ptr %2, align 4
  %3 = load i32, ptr %2, align 4
  %4 = call i32 (ptr, ...) @printf(ptr noundef @.str.3, i32 noundef %3) #2
  ret void
}

; Function Attrs: noinline nounwind optnone
define dso_local ptr @getString() #0 {
  %1 = alloca ptr, align 4
  %2 = call ptr @malloc(i32 noundef 4096) #2
  store ptr %2, ptr %1, align 4
  %3 = load ptr, ptr %1, align 4
  %4 = call i32 (ptr, ...) @scanf(ptr noundef @.str, ptr noundef %3) #3
  %5 = load ptr, ptr %1, align 4
  ret ptr %5
}

declare dso_local ptr @malloc(i32 noundef) #1

declare dso_local i32 @scanf(ptr noundef, ...) #1

; Function Attrs: noinline nounwind optnone
define dso_local i32 @getInt() #0 {
  %1 = alloca i32, align 4
  %2 = call i32 (ptr, ...) @scanf(ptr noundef @.str.2, ptr noundef %1) #3
  %3 = load i32, ptr %1, align 4
  ret i32 %3
}

; Function Attrs: noinline nounwind optnone
define dso_local ptr @toString(i32 noundef %0) #0 {
  %2 = alloca i32, align 4
  %3 = alloca ptr, align 4
  store i32 %0, ptr %2, align 4
  %4 = call ptr @malloc(i32 noundef 16) #2
  store ptr %4, ptr %3, align 4
  %5 = load ptr, ptr %3, align 4
  %6 = load i32, ptr %2, align 4
  %7 = call i32 (ptr, ptr, ...) @sprintf(ptr noundef %5, ptr noundef @.str.2, i32 noundef %6) #3
  %8 = load ptr, ptr %3, align 4
  ret ptr %8
}

declare dso_local i32 @sprintf(ptr noundef, ptr noundef, ...) #1

; Function Attrs: noinline nounwind optnone
define dso_local ptr @string.string() #0 {
  %1 = alloca ptr, align 4
  %2 = call ptr @malloc(i32 noundef 1) #2
  store ptr %2, ptr %1, align 4
  %3 = load ptr, ptr %1, align 4
  %4 = getelementptr inbounds i8, ptr %3, i32 0
  store i8 0, ptr %4, align 1
  %5 = load ptr, ptr %1, align 4
  ret ptr %5
}

; Function Attrs: noinline nounwind optnone
define dso_local i32 @string.length(ptr noundef %0) #0 {
  %2 = alloca ptr, align 4
  store ptr %0, ptr %2, align 4
  %3 = load ptr, ptr %2, align 4
  %4 = call i32 @strlen(ptr noundef %3) #2
  ret i32 %4
}

declare dso_local i32 @strlen(ptr noundef) #1

; Function Attrs: noinline nounwind optnone
define dso_local ptr @string.substring(ptr noundef %0, i32 noundef %1, i32 noundef %2) #0 {
  %4 = alloca ptr, align 4
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = alloca ptr, align 4
  store ptr %0, ptr %4, align 4
  store i32 %1, ptr %5, align 4
  store i32 %2, ptr %6, align 4
  %9 = load i32, ptr %6, align 4
  %10 = load i32, ptr %5, align 4
  %11 = sub nsw i32 %9, %10
  store i32 %11, ptr %7, align 4
  %12 = load i32, ptr %7, align 4
  %13 = add nsw i32 %12, 1
  %14 = call ptr @malloc(i32 noundef %13) #2
  store ptr %14, ptr %8, align 4
  %15 = load ptr, ptr %8, align 4
  %16 = load ptr, ptr %4, align 4
  %17 = load i32, ptr %5, align 4
  %18 = getelementptr inbounds i8, ptr %16, i32 %17
  %19 = load i32, ptr %7, align 4
  %20 = call ptr @memcpy(ptr noundef %15, ptr noundef %18, i32 noundef %19) #2
  %21 = load ptr, ptr %8, align 4
  %22 = load i32, ptr %7, align 4
  %23 = getelementptr inbounds i8, ptr %21, i32 %22
  store i8 0, ptr %23, align 1
  %24 = load ptr, ptr %8, align 4
  ret ptr %24
}

declare dso_local ptr @memcpy(ptr noundef, ptr noundef, i32 noundef) #1

; Function Attrs: noinline nounwind optnone
define dso_local i32 @string.parseInt(ptr noundef %0) #0 {
  %2 = alloca ptr, align 4
  %3 = alloca i32, align 4
  store ptr %0, ptr %2, align 4
  %4 = load ptr, ptr %2, align 4
  %5 = call i32 (ptr, ptr, ...) @sscanf(ptr noundef %4, ptr noundef @.str.2, ptr noundef %3) #3
  %6 = load i32, ptr %3, align 4
  ret i32 %6
}

declare dso_local i32 @sscanf(ptr noundef, ptr noundef, ...) #1

; Function Attrs: noinline nounwind optnone
define dso_local i32 @string.ord(ptr noundef %0, i32 noundef %1) #0 {
  %3 = alloca ptr, align 4
  %4 = alloca i32, align 4
  store ptr %0, ptr %3, align 4
  store i32 %1, ptr %4, align 4
  %5 = load ptr, ptr %3, align 4
  %6 = load i32, ptr %4, align 4
  %7 = getelementptr inbounds i8, ptr %5, i32 %6
  %8 = load i8, ptr %7, align 1
  %9 = zext i8 %8 to i32
  ret i32 %9
}

; Function Attrs: noinline nounwind optnone
define dso_local ptr @string.add(ptr noundef %0, ptr noundef %1) #0 {
  %3 = alloca ptr, align 4
  %4 = alloca ptr, align 4
  %5 = alloca i32, align 4
  %6 = alloca i32, align 4
  %7 = alloca i32, align 4
  %8 = alloca ptr, align 4
  store ptr %0, ptr %3, align 4
  store ptr %1, ptr %4, align 4
  %9 = load ptr, ptr %3, align 4
  %10 = call i32 @strlen(ptr noundef %9) #2
  store i32 %10, ptr %5, align 4
  %11 = load ptr, ptr %4, align 4
  %12 = call i32 @strlen(ptr noundef %11) #2
  store i32 %12, ptr %6, align 4
  %13 = load i32, ptr %5, align 4
  %14 = load i32, ptr %6, align 4
  %15 = add nsw i32 %13, %14
  store i32 %15, ptr %7, align 4
  %16 = load i32, ptr %7, align 4
  %17 = add nsw i32 %16, 1
  %18 = call ptr @malloc(i32 noundef %17) #2
  store ptr %18, ptr %8, align 4
  %19 = load ptr, ptr %8, align 4
  %20 = load ptr, ptr %3, align 4
  %21 = load i32, ptr %5, align 4
  %22 = call ptr @memcpy(ptr noundef %19, ptr noundef %20, i32 noundef %21) #2
  %23 = load ptr, ptr %8, align 4
  %24 = load i32, ptr %5, align 4
  %25 = getelementptr inbounds i8, ptr %23, i32 %24
  %26 = load ptr, ptr %4, align 4
  %27 = load i32, ptr %6, align 4
  %28 = call ptr @memcpy(ptr noundef %25, ptr noundef %26, i32 noundef %27) #2
  %29 = load ptr, ptr %8, align 4
  %30 = load i32, ptr %7, align 4
  %31 = getelementptr inbounds i8, ptr %29, i32 %30
  store i8 0, ptr %31, align 1
  %32 = load ptr, ptr %8, align 4
  ret ptr %32
}

; Function Attrs: noinline nounwind optnone
define dso_local zeroext i1 @string.equal(ptr noundef %0, ptr noundef %1) #0 {
  %3 = alloca ptr, align 4
  %4 = alloca ptr, align 4
  store ptr %0, ptr %3, align 4
  store ptr %1, ptr %4, align 4
  %5 = load ptr, ptr %3, align 4
  %6 = load ptr, ptr %4, align 4
  %7 = call i32 @strcmp(ptr noundef %5, ptr noundef %6) #3
  %8 = icmp eq i32 %7, 0
  ret i1 %8
}

declare dso_local i32 @strcmp(ptr noundef, ptr noundef) #1

; Function Attrs: noinline nounwind optnone
define dso_local zeroext i1 @string.notEqual(ptr noundef %0, ptr noundef %1) #0 {
  %3 = alloca ptr, align 4
  %4 = alloca ptr, align 4
  store ptr %0, ptr %3, align 4
  store ptr %1, ptr %4, align 4
  %5 = load ptr, ptr %3, align 4
  %6 = load ptr, ptr %4, align 4
  %7 = call i32 @strcmp(ptr noundef %5, ptr noundef %6) #3
  %8 = icmp ne i32 %7, 0
  ret i1 %8
}

; Function Attrs: noinline nounwind optnone
define dso_local zeroext i1 @string.less(ptr noundef %0, ptr noundef %1) #0 {
  %3 = alloca ptr, align 4
  %4 = alloca ptr, align 4
  store ptr %0, ptr %3, align 4
  store ptr %1, ptr %4, align 4
  %5 = load ptr, ptr %3, align 4
  %6 = load ptr, ptr %4, align 4
  %7 = call i32 @strcmp(ptr noundef %5, ptr noundef %6) #3
  %8 = icmp slt i32 %7, 0
  ret i1 %8
}

; Function Attrs: noinline nounwind optnone
define dso_local zeroext i1 @string.lessOrEqual(ptr noundef %0, ptr noundef %1) #0 {
  %3 = alloca ptr, align 4
  %4 = alloca ptr, align 4
  store ptr %0, ptr %3, align 4
  store ptr %1, ptr %4, align 4
  %5 = load ptr, ptr %3, align 4
  %6 = load ptr, ptr %4, align 4
  %7 = call i32 @strcmp(ptr noundef %5, ptr noundef %6) #3
  %8 = icmp sle i32 %7, 0
  ret i1 %8
}

; Function Attrs: noinline nounwind optnone
define dso_local zeroext i1 @string.greater(ptr noundef %0, ptr noundef %1) #0 {
  %3 = alloca ptr, align 4
  %4 = alloca ptr, align 4
  store ptr %0, ptr %3, align 4
  store ptr %1, ptr %4, align 4
  %5 = load ptr, ptr %3, align 4
  %6 = load ptr, ptr %4, align 4
  %7 = call i32 @strcmp(ptr noundef %5, ptr noundef %6) #3
  %8 = icmp sgt i32 %7, 0
  ret i1 %8
}

; Function Attrs: noinline nounwind optnone
define dso_local zeroext i1 @string.greaterOrEqual(ptr noundef %0, ptr noundef %1) #0 {
  %3 = alloca ptr, align 4
  %4 = alloca ptr, align 4
  store ptr %0, ptr %3, align 4
  store ptr %1, ptr %4, align 4
  %5 = load ptr, ptr %3, align 4
  %6 = load ptr, ptr %4, align 4
  %7 = call i32 @strcmp(ptr noundef %5, ptr noundef %6) #3
  %8 = icmp sge i32 %7, 0
  ret i1 %8
}

; Function Attrs: noinline nounwind optnone
define dso_local i32 @__array.size(ptr noundef %0) #0 {
  %2 = alloca ptr, align 4
  store ptr %0, ptr %2, align 4
  %3 = load ptr, ptr %2, align 4
  %4 = getelementptr inbounds i32, ptr %3, i32 -1
  %5 = load i32, ptr %4, align 4
  ret i32 %5
}

; Function Attrs: noinline nounwind optnone
define dso_local ptr @__newPtrArray(i32 noundef %0) #0 {
  %2 = alloca i32, align 4
  %3 = alloca ptr, align 4
  store i32 %0, ptr %2, align 4
  %4 = load i32, ptr %2, align 4
  %5 = shl i32 %4, 2
  %6 = add nsw i32 %5, 4
  %7 = call ptr @malloc(i32 noundef %6) #2
  store ptr %7, ptr %3, align 4
  %8 = load i32, ptr %2, align 4
  %9 = load ptr, ptr %3, align 4
  %10 = getelementptr inbounds i32, ptr %9, i32 0
  store i32 %8, ptr %10, align 4
  %11 = load ptr, ptr %3, align 4
  %12 = getelementptr inbounds i32, ptr %11, i32 1
  ret ptr %12
}

; Function Attrs: noinline nounwind optnone
define dso_local ptr @__newIntArray(i32 noundef %0) #0 {
  %2 = alloca i32, align 4
  %3 = alloca ptr, align 4
  store i32 %0, ptr %2, align 4
  %4 = load i32, ptr %2, align 4
  %5 = shl i32 %4, 2
  %6 = add nsw i32 %5, 4
  %7 = call ptr @malloc(i32 noundef %6) #2
  store ptr %7, ptr %3, align 4
  %8 = load i32, ptr %2, align 4
  %9 = load ptr, ptr %3, align 4
  %10 = getelementptr inbounds i32, ptr %9, i32 0
  store i32 %8, ptr %10, align 4
  %11 = load ptr, ptr %3, align 4
  %12 = getelementptr inbounds i32, ptr %11, i32 1
  ret ptr %12
}

; Function Attrs: noinline nounwind optnone
define dso_local ptr @__newBoolArray(i32 noundef %0) #0 {
  %2 = alloca i32, align 4
  %3 = alloca ptr, align 4
  store i32 %0, ptr %2, align 4
  %4 = load i32, ptr %2, align 4
  %5 = add nsw i32 %4, 4
  %6 = call ptr @malloc(i32 noundef %5) #2
  store ptr %6, ptr %3, align 4
  %7 = load i32, ptr %2, align 4
  %8 = load ptr, ptr %3, align 4
  %9 = getelementptr inbounds i32, ptr %8, i32 0
  store i32 %7, ptr %9, align 4
  %10 = load ptr, ptr %3, align 4
  %11 = getelementptr inbounds i32, ptr %10, i32 1
  ret ptr %11
}

attributes #0 = { noinline nounwind optnone "frame-pointer"="all" "min-legal-vector-width"="0" "no-builtin-malloc" "no-builtin-memcpy" "no-builtin-printf" "no-builtin-strlen" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-features"="+a,+c,+m,+relax,-save-restore" }
attributes #1 = { "frame-pointer"="all" "no-builtin-malloc" "no-builtin-memcpy" "no-builtin-printf" "no-builtin-strlen" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-features"="+a,+c,+m,+relax,-save-restore" }
attributes #2 = { nobuiltin "no-builtin-malloc" "no-builtin-memcpy" "no-builtin-printf" "no-builtin-strlen" }
attributes #3 = { "no-builtin-malloc" "no-builtin-memcpy" "no-builtin-printf" "no-builtin-strlen" }

!llvm.module.flags = !{!0, !1, !2, !3}
!llvm.ident = !{!4}

!0 = !{i32 1, !"wchar_size", i32 4}
!1 = !{i32 1, !"target-abi", !"ilp32"}
!2 = !{i32 7, !"frame-pointer", i32 2}
!3 = !{i32 1, !"SmallDataLimit", i32 8}
!4 = !{!"Ubuntu clang version 15.0.7"}

; ModuleID = 'builtin.c'
source_filename = "builtin.c"
target datalayout = "e-m:e-p:32:32-p270:32:32-p271:32:32-p272:64:64-f64:32:64-f80:32-n8:16:32-S128"
target triple = "i386-pc-linux-gnu"

@.str = private unnamed_addr constant [3 x i8] c"%s\00", align 1
@.str.2 = private unnamed_addr constant [3 x i8] c"%d\00", align 1
@.str.3 = private unnamed_addr constant [4 x i8] c"%d\0A\00", align 1

; Function Attrs: nofree nounwind sspstrong uwtable
define dso_local void @print(ptr noundef %str) local_unnamed_addr #0 {
entry:
  %call = tail call i32 (ptr, ...) @printf(ptr noundef nonnull @.str, ptr noundef %str)
  ret void
}

; Function Attrs: nofree nounwind
declare noundef i32 @printf(ptr nocapture noundef readonly, ...) local_unnamed_addr #1

; Function Attrs: nofree nounwind sspstrong uwtable
define dso_local void @println(ptr nocapture noundef readonly %str) local_unnamed_addr #0 {
entry:
  %puts = tail call i32 @puts(ptr nonnull dereferenceable(1) %str)
  ret void
}

; Function Attrs: nofree nounwind sspstrong uwtable
define dso_local void @printInt(i32 noundef %n) local_unnamed_addr #0 {
entry:
  %call = tail call i32 (ptr, ...) @printf(ptr noundef nonnull @.str.2, i32 noundef %n)
  ret void
}

; Function Attrs: nofree nounwind sspstrong uwtable
define dso_local void @printlnInt(i32 noundef %n) local_unnamed_addr #0 {
entry:
  %call = tail call i32 (ptr, ...) @printf(ptr noundef nonnull @.str.3, i32 noundef %n)
  ret void
}

; Function Attrs: nofree nounwind sspstrong uwtable
define dso_local ptr @getString() local_unnamed_addr #0 {
entry:
  %call = tail call dereferenceable_or_null(4096) ptr @malloc(i32 noundef 4096) #10
  %call1 = tail call i32 (ptr, ...) @scanf(ptr noundef nonnull @.str, ptr noundef %call)
  ret ptr %call
}

; Function Attrs: argmemonly mustprogress nocallback nofree nosync nounwind willreturn
declare void @llvm.lifetime.start.p0(i64 immarg, ptr nocapture) #2

; Function Attrs: inaccessiblememonly mustprogress nofree nounwind willreturn allockind("alloc,uninitialized") allocsize(0)
declare noalias noundef ptr @malloc(i32 noundef) local_unnamed_addr #3

; Function Attrs: nofree nounwind
declare noundef i32 @scanf(ptr nocapture noundef readonly, ...) local_unnamed_addr #1

; Function Attrs: argmemonly mustprogress nocallback nofree nosync nounwind willreturn
declare void @llvm.lifetime.end.p0(i64 immarg, ptr nocapture) #2

; Function Attrs: nofree nounwind sspstrong uwtable
define dso_local i32 @getInt() local_unnamed_addr #0 {
entry:
  %n = alloca i32, align 4
  call void @llvm.lifetime.start.p0(i64 4, ptr nonnull %n) #11
  %call = call i32 (ptr, ...) @scanf(ptr noundef nonnull @.str.2, ptr noundef nonnull %n)
  %0 = load i32, ptr %n, align 4, !tbaa !6
  call void @llvm.lifetime.end.p0(i64 4, ptr nonnull %n) #11
  ret i32 %0
}

; Function Attrs: nofree nounwind sspstrong uwtable
define dso_local noalias ptr @toString(i32 noundef %n) local_unnamed_addr #0 {
entry:
  %call = tail call dereferenceable_or_null(16) ptr @malloc(i32 noundef 16) #10
  %call1 = tail call i32 (ptr, ptr, ...) @sprintf(ptr noundef nonnull dereferenceable(1) %call, ptr noundef nonnull @.str.2, i32 noundef %n)
  ret ptr %call
}

; Function Attrs: nofree nounwind
declare noundef i32 @sprintf(ptr noalias nocapture noundef writeonly, ptr nocapture noundef readonly, ...) local_unnamed_addr #1

; Function Attrs: mustprogress nofree nounwind sspstrong willreturn uwtable
define dso_local noalias ptr @string.string() local_unnamed_addr #4 {
entry:
  %call = tail call dereferenceable_or_null(1) ptr @malloc(i32 noundef 1) #10
  store i8 0, ptr %call, align 1, !tbaa !10
  ret ptr %call
}

; Function Attrs: argmemonly mustprogress nofree nounwind readonly sspstrong willreturn uwtable
define dso_local i32 @string.length(ptr nocapture noundef readonly %__this) local_unnamed_addr #5 {
entry:
  %call = tail call i32 @strlen(ptr noundef nonnull dereferenceable(1) %__this)
  ret i32 %call
}

; Function Attrs: argmemonly mustprogress nofree nounwind readonly willreturn
declare i32 @strlen(ptr nocapture noundef) local_unnamed_addr #6

; Function Attrs: mustprogress nofree nounwind sspstrong willreturn uwtable
define dso_local noalias ptr @string.substring(ptr nocapture noundef readonly %__this, i32 noundef %left, i32 noundef %right) local_unnamed_addr #4 {
entry:
  %sub = sub nsw i32 %right, %left
  %add = add nsw i32 %sub, 1
  %call = tail call ptr @malloc(i32 noundef %add) #10
  %add.ptr = getelementptr inbounds i8, ptr %__this, i32 %left
  tail call void @llvm.memcpy.p0.p0.i32(ptr align 1 %call, ptr align 1 %add.ptr, i32 %sub, i1 false)
  %arrayidx = getelementptr inbounds i8, ptr %call, i32 %sub
  store i8 0, ptr %arrayidx, align 1, !tbaa !10
  ret ptr %call
}

; Function Attrs: argmemonly mustprogress nocallback nofree nounwind willreturn
declare void @llvm.memcpy.p0.p0.i32(ptr noalias nocapture writeonly, ptr noalias nocapture readonly, i32, i1 immarg) #7

; Function Attrs: nofree nounwind sspstrong uwtable
define dso_local i32 @string.parseInt(ptr nocapture noundef readonly %__this) local_unnamed_addr #0 {
entry:
  %n = alloca i32, align 4
  call void @llvm.lifetime.start.p0(i64 4, ptr nonnull %n) #11
  %call = call i32 (ptr, ptr, ...) @sscanf(ptr noundef %__this, ptr noundef nonnull @.str.2, ptr noundef nonnull %n)
  %0 = load i32, ptr %n, align 4, !tbaa !6
  call void @llvm.lifetime.end.p0(i64 4, ptr nonnull %n) #11
  ret i32 %0
}

; Function Attrs: nofree nounwind
declare noundef i32 @sscanf(ptr nocapture noundef readonly, ptr nocapture noundef readonly, ...) local_unnamed_addr #1

; Function Attrs: argmemonly mustprogress nofree norecurse nosync nounwind readonly sspstrong willreturn uwtable
define dso_local i32 @string.ord(ptr nocapture noundef readonly %__this, i32 noundef %pos) local_unnamed_addr #8 {
entry:
  %arrayidx = getelementptr inbounds i8, ptr %__this, i32 %pos
  %0 = load i8, ptr %arrayidx, align 1, !tbaa !10
  %conv = sext i8 %0 to i32
  ret i32 %conv
}

; Function Attrs: mustprogress nofree nounwind sspstrong willreturn uwtable
define dso_local noalias ptr @string.add(ptr nocapture noundef readonly %str1, ptr nocapture noundef readonly %str2) local_unnamed_addr #4 {
entry:
  %call = tail call i32 @strlen(ptr noundef nonnull dereferenceable(1) %str1)
  %call1 = tail call i32 @strlen(ptr noundef nonnull dereferenceable(1) %str2)
  %add = add nsw i32 %call1, %call
  %add2 = add nsw i32 %add, 1
  %call3 = tail call ptr @malloc(i32 noundef %add2) #10
  tail call void @llvm.memcpy.p0.p0.i32(ptr align 1 %call3, ptr align 1 %str1, i32 %call, i1 false)
  %add.ptr = getelementptr inbounds i8, ptr %call3, i32 %call
  tail call void @llvm.memcpy.p0.p0.i32(ptr align 1 %add.ptr, ptr align 1 %str2, i32 %call1, i1 false)
  %arrayidx = getelementptr inbounds i8, ptr %call3, i32 %add
  store i8 0, ptr %arrayidx, align 1, !tbaa !10
  ret ptr %call3
}

; Function Attrs: argmemonly mustprogress nofree nounwind readonly sspstrong willreturn uwtable
define dso_local zeroext i1 @string.equal(ptr nocapture noundef readonly %str1, ptr nocapture noundef readonly %str2) local_unnamed_addr #5 {
entry:
  %call = tail call i32 @strcmp(ptr noundef nonnull dereferenceable(1) %str1, ptr noundef nonnull dereferenceable(1) %str2)
  %cmp = icmp eq i32 %call, 0
  ret i1 %cmp
}

; Function Attrs: argmemonly mustprogress nofree nounwind readonly willreturn
declare i32 @strcmp(ptr nocapture noundef, ptr nocapture noundef) local_unnamed_addr #6

; Function Attrs: argmemonly mustprogress nofree nounwind readonly sspstrong willreturn uwtable
define dso_local zeroext i1 @string.notEqual(ptr nocapture noundef readonly %str1, ptr nocapture noundef readonly %str2) local_unnamed_addr #5 {
entry:
  %call = tail call i32 @strcmp(ptr noundef nonnull dereferenceable(1) %str1, ptr noundef nonnull dereferenceable(1) %str2)
  %cmp = icmp ne i32 %call, 0
  ret i1 %cmp
}

; Function Attrs: argmemonly mustprogress nofree nounwind readonly sspstrong willreturn uwtable
define dso_local zeroext i1 @string.less(ptr nocapture noundef readonly %str1, ptr nocapture noundef readonly %str2) local_unnamed_addr #5 {
entry:
  %call = tail call i32 @strcmp(ptr noundef nonnull dereferenceable(1) %str1, ptr noundef nonnull dereferenceable(1) %str2)
  %cmp = icmp slt i32 %call, 0
  ret i1 %cmp
}

; Function Attrs: argmemonly mustprogress nofree nounwind readonly sspstrong willreturn uwtable
define dso_local zeroext i1 @string.lessOrEqual(ptr nocapture noundef readonly %str1, ptr nocapture noundef readonly %str2) local_unnamed_addr #5 {
entry:
  %call = tail call i32 @strcmp(ptr noundef nonnull dereferenceable(1) %str1, ptr noundef nonnull dereferenceable(1) %str2)
  %cmp = icmp slt i32 %call, 1
  ret i1 %cmp
}

; Function Attrs: argmemonly mustprogress nofree nounwind readonly sspstrong willreturn uwtable
define dso_local zeroext i1 @string.greater(ptr nocapture noundef readonly %str1, ptr nocapture noundef readonly %str2) local_unnamed_addr #5 {
entry:
  %call = tail call i32 @strcmp(ptr noundef nonnull dereferenceable(1) %str1, ptr noundef nonnull dereferenceable(1) %str2)
  %cmp = icmp sgt i32 %call, 0
  ret i1 %cmp
}

; Function Attrs: argmemonly mustprogress nofree nounwind readonly sspstrong willreturn uwtable
define dso_local zeroext i1 @string.greaterOrEqual(ptr nocapture noundef readonly %str1, ptr nocapture noundef readonly %str2) local_unnamed_addr #5 {
entry:
  %call = tail call i32 @strcmp(ptr noundef nonnull dereferenceable(1) %str1, ptr noundef nonnull dereferenceable(1) %str2)
  %cmp = icmp sgt i32 %call, -1
  ret i1 %cmp
}

; Function Attrs: argmemonly mustprogress nofree norecurse nosync nounwind readonly sspstrong willreturn uwtable
define dso_local i32 @__array.size(ptr nocapture noundef readonly %__this) local_unnamed_addr #8 {
entry:
  %arrayidx = getelementptr inbounds i32, ptr %__this, i32 -1
  %0 = load i32, ptr %arrayidx, align 4, !tbaa !6
  ret i32 %0
}

; Function Attrs: mustprogress nofree nounwind sspstrong willreturn uwtable
define dso_local noalias nonnull ptr @__newPtrArray(i32 noundef %size) local_unnamed_addr #4 {
entry:
  %shl = shl i32 %size, 2
  %add = add nsw i32 %shl, 4
  %call = tail call ptr @malloc(i32 noundef %add) #10
  store i32 %size, ptr %call, align 4, !tbaa !6
  %add.ptr = getelementptr inbounds i32, ptr %call, i32 1
  ret ptr %add.ptr
}

; Function Attrs: mustprogress nofree nounwind sspstrong willreturn uwtable
define dso_local noalias nonnull ptr @__newIntArray(i32 noundef %size) local_unnamed_addr #4 {
entry:
  %shl = shl i32 %size, 2
  %add = add nsw i32 %shl, 4
  %call = tail call ptr @malloc(i32 noundef %add) #10
  store i32 %size, ptr %call, align 4, !tbaa !6
  %add.ptr = getelementptr inbounds i32, ptr %call, i32 1
  ret ptr %add.ptr
}

; Function Attrs: mustprogress nofree nounwind sspstrong willreturn uwtable
define dso_local noalias nonnull ptr @__newBoolArray(i32 noundef %size) local_unnamed_addr #4 {
entry:
  %add = add nsw i32 %size, 4
  %call = tail call ptr @malloc(i32 noundef %add) #10
  store i32 %size, ptr %call, align 4, !tbaa !6
  %add.ptr = getelementptr inbounds i32, ptr %call, i32 1
  ret ptr %add.ptr
}

; Function Attrs: nofree nounwind
declare noundef i32 @puts(ptr nocapture noundef readonly) local_unnamed_addr #9

attributes #0 = { nofree nounwind sspstrong uwtable "frame-pointer"="none" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="pentium4" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #1 = { nofree nounwind "frame-pointer"="none" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="pentium4" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #2 = { argmemonly mustprogress nocallback nofree nosync nounwind willreturn }
attributes #3 = { inaccessiblememonly mustprogress nofree nounwind willreturn allockind("alloc,uninitialized") allocsize(0) "alloc-family"="malloc" "frame-pointer"="none" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="pentium4" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #4 = { mustprogress nofree nounwind sspstrong willreturn uwtable "frame-pointer"="none" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="pentium4" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #5 = { argmemonly mustprogress nofree nounwind readonly sspstrong willreturn uwtable "frame-pointer"="none" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="pentium4" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #6 = { argmemonly mustprogress nofree nounwind readonly willreturn "frame-pointer"="none" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="pentium4" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #7 = { argmemonly mustprogress nocallback nofree nounwind willreturn }
attributes #8 = { argmemonly mustprogress nofree norecurse nosync nounwind readonly sspstrong willreturn uwtable "frame-pointer"="none" "min-legal-vector-width"="0" "no-trapping-math"="true" "stack-protector-buffer-size"="8" "target-cpu"="pentium4" "target-features"="+cx8,+fxsr,+mmx,+sse,+sse2,+x87" "tune-cpu"="generic" }
attributes #9 = { nofree nounwind }
attributes #10 = { allocsize(0) }
attributes #11 = { nounwind }

!llvm.module.flags = !{!0, !1, !2, !3, !4}
!llvm.ident = !{!5}

!0 = !{i32 1, !"NumRegisterParameters", i32 0}
!1 = !{i32 1, !"wchar_size", i32 4}
!2 = !{i32 7, !"PIC Level", i32 2}
!3 = !{i32 7, !"PIE Level", i32 2}
!4 = !{i32 7, !"uwtable", i32 2}
!5 = !{!"clang version 15.0.7"}
!6 = !{!7, !7, i64 0}
!7 = !{!"int", !8, i64 0}
!8 = !{!"omnipotent char", !9, i64 0}
!9 = !{!"Simple C/C++ TBAA"}
!10 = !{!8, !8, i64 0}
# How To Use

```
llvm-link-15 buildin.ll output.ll -o link.bc
llvm-dis-15 link.bc
clang-15 link.bc -o test
./test
$?
```


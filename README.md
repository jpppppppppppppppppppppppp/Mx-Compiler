# How To Use

```
clang-15 -m32 builtin.ll output.ll -o test
./test
$?
```

| testcase | simulate time(without any opt) | simulate time(mem2reg & regalloc) |
| :--: | :--: | :--: |
|e1.mx| 103911 | 46477 |
|e10.mx| 3511 | 1335 |
|e2.mx| 88593 | 16104 |
|e3.mx| 2113 | 1153 |
|e4.mx| 5667 | 3168 |
|e5.mx| 46195 | 37116 |
|e6.mx| 24172 | 11107 |
|e7.mx| 9915 | 5176 |
|e8.mx| 51723 | 21672 |
|e9.mx| 15891 | 8082 |
|dijkstra.mx| 6427558328 | 1171275097 |
|floyd.mx| 4315673101 | 740382745 |
|spfa.mx| 4450265867 | 913215459 |
|bubble_sort.mx| 23421370 | 2105504 |
|merge_sort.mx| 95633447 | 18153885 |
|quick_sort.mx| 3560436 | 683818 |
|selection_sort.mx| 12157591 | 1210638 |
|queue.mt| 3129816 | 959415 |
|t1.mx| 703150083 | 37292970 |
|t10.mx| 15499 | 6364 |
|t11.mx| 19542 | 173 |
|t12.mx| 2147290 | 809916 |
|t13.mx| 4934 | 3521 |
|t14.mx| 33509 | 25100 |
|t15.mx| 58922698 | 4187348 |
|t16.mx| 10328 | 4964 |
|t17.mx| 1316589273 | 50297806 |
|t18.mx| 32231297 | 10447903 |
|t19.mx| 144960 | 43656 |
|t2.mx| 73926201 | 14179923 |
|t20.mx| 509371988 | 34883006 |
|t21.mx| 277262287 | 49013302 |
|t22.mx| 338210 | 147874 |
|t23.mx| 11428877 | 8425152 |
|t24.mx| 107312345 | 21206727 |
|t25.mx| 119923179 | 16391442 |
|t26.mx| 961163294 | 252044855 |
|t27.mx| 102499498 | 27480536 |
|t28.mx| 15499 | 6364 |
|t29.mx| 15499 | 6364 |
|t3.mx| 773463638 | 186955637 |
|t30.mx| 121436582 | 48054469 |
|t31.mx| 304116814 | 87101145 |
|t32.mx| 3934827 | 819760 |
|t33.mx| 1743 | 5 |
|t34.mx| 5360 | 3827 |
|t35.mx| 1621 | 8 |
|t36.mx| 2977 | 660 |
|t37.mx| 2592 | 1823 |
|t38.mx| 31086 | 339 |
|t39.mx| 2394 | 150 |
|t4.mx| 1079132763 | 193663146 |
|t40.mx| 2265 | 1432 |
|t41.mx| 4536 | 931 |
|t42.mx| 1558 | 400 |
|t43.mx| 1109 | 7 |
|t44.mx| 121432685 | 48051786 |
|t45.mx| 2268 | 1110 |
|t46.mx| 46166 | 535 |
|t47.mx| 2181 | 53 |
|t48.mx| 714 | 135 |
|t49.mx| 3297 | 2208 |
|t5.mx| 2254 | 5 |
|t50.mx| 33125 | 353 |
|t51.mx| 48096 | 550 |
|t52.mx| 21715 | 1807 |
|t53.mx| 70763 | 6547 |
|t54.mx| 2758 | 53 |
|t55.mx| 2470770 | 1926738 |
|t56.mx| 123698 | 27089 |
|t57.mx| 59636583 | 1180667 |
|t58.mx| 179524584476 | 14404306786 |
|t59.mx| 54649505558 | 5231371034 |
|t6.mx| 1612 | 5 |
|t60.mx| 790860024 | 9264150 |
|t61.mx| 698019 | 329665 |
|t62.mx| 1358 | 267 |
|t63.mx| 237263 | 127199 |
|t64.mx| 4607829 | 3371467 |
|t66.mx| 2008 | 469 |
|t67.mx| 245114 | 214075 |
|t68.mx| 108397 | 26784 |
|t69.mx| 177805 | 52345 |
|t7.mx| 46903 | 24618 |
|t70.mx| 146715 | 34870 |
|t71.mx| 8252 | 3584 |
|t72.mx| 5019 | 2076 |
|t73.mx| 7298 | 3845 |
|t8.mx| 63948 | 29164 |
|t9.mx| 13639 | 1606 |


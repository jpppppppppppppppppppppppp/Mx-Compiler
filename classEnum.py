from enum import Enum


class llvmEnum(Enum):
    Alloca = 0
    GlobalString = 1
    ClassType = 2
    Load = 3
    Return = 4
    ReturnVoid = 5
    GlobalVar = 6
    Getelementptr1 = 7
    Getelementptr2 = 8
    Label = 9
    Jump = 10
    Trunc = 11
    Br = 12
    Zext = 13
    Phi = 14
    Icmp = 15
    Store = 16
    Binary = 17
    FuncCall = 18
    FuncVoid = 19
    Pass = 20

    def __eq__(self, other):
        return self.value == other.value


class lrEnum(Enum):
    mv = 0
    lw = 1
    label = 2
    binary = 3
    li = 4
    ret = 5
    call = 6
    sw = 7
    lui = 8
    icmp = 9
    j = 10
    bnez = 11
    binaryi = 12

    def __eq__(self, other):
        return self.value == other.value

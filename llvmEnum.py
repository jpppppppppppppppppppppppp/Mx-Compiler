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

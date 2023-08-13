from main import llvmEnum


class Regtrival:
    def __init__(self):
        self.Vars2addr = {}
        self.Vars2Reg = {}
        self.Unused = []
        self.Regtouse = ['t1', 't2', 't3']

    def alloca(self, varname):
        if varname not in self.Vars2addr and len(self.Unused) > 0:
            addr = self.Unused.pop(0)
            self.Vars2addr[varname] = addr
        else:
            raise Exception("Warning")

    def var2Reg(self, array, var):
        if var.isdigit():
            reg = self.Regtouse.pop(0)
            array.append(f'\tli\t{reg}, {var}\n')
            return reg, [reg]
        elif var[0] == '%':
            print('reg', var, 'todo')
        elif var[0] == '@':
            print('reg', var, 'todo')
        else:
            raise Exception("Warning")
        return None, []

    def var2Addr(self, array, tar):
        if tar[0] == '%':
            if tar in self.Vars2addr:
                return str(self.Vars2addr[tar]) + '(sp)', []
            else:
                raise Exception("Warning")
        else:
            print('addr', tar)
        return None, []

    def store(self, array, reg, addr, clean):
        array.append(f"\tsw\t{reg}, {addr}\n")
        for toclean in clean:
            self.Regtouse.append(toclean)


class RISCV:
    def __init__(self, filename):
        self.output = open(filename, 'w')
        self.Reg = Regtrival()
        self.globalvar = []
        self.func = []
        self.end = False

    def translateglobalvars(self, array):
        if array[0] == llvmEnum.GlobalVar:
            self.globalvar.append([])
            if type(array[3]).__name__ == 'str' and array[3][0] == '@':
                self.globalvar[-1].append(f'.{array[1]}:\n')
                self.globalvar[-1].append(f'\t.word {array[3][1:]}\n')
            else:
                self.globalvar[-1].append(f'.{array[1]}:\n')
                self.globalvar[-1].append(f'\t.word {array[3]}\n')
        elif array[0] == llvmEnum.GlobalString:
            self.globalvar.append([])
            if array[2] == 1:
                self.globalvar[-1].append(f'.string.{array[1]}:\n')
                self.globalvar[-1].append(f'\t.zero 1\n')
            else:
                self.globalvar[-1].append(f'.string.{array[1]}:\n')
                self.globalvar[-1].append(f'\t.asciz \"{array[3]}\"\n')
        else:
            pass

    def translatefunction(self, funcname, array):
        if funcname != 'main':
            raise Exception("TODO")
        else:
            needReg = []
            needpc = array[3]
        self.func.append([f"\t.global {funcname}\n", f"{funcname}:\t\t# @{funcname}\n"])
        self.init(needReg, (needpc + 3) & ~3)
        for block in array[2]:
            self.translateblock(block)

    def translateblock(self, array):
        self.end = False
        for smt in array:
            self.translatesmt(smt)

    def translatesmt(self, smt):
        if self.end:
            pass
        if smt[0] == llvmEnum.Label:
            self.func[-1].append(f".{smt[1]}\t\t# %{smt[1]}\n")
        elif smt[0] == llvmEnum.Alloca:
            self.Reg.alloca(smt[1])
        elif smt[0] == llvmEnum.Store:
            temp = []
            varReg, clean = self.Reg.var2Reg(self.func[-1], smt[2])
            for toclear in clean:
                temp.append(toclear)
            taraddr, clean = self.Reg.var2Addr(self.func[-1], smt[3])
            for toclear in clean:
                temp.append(toclear)
            self.Reg.store(self.func[-1], varReg, taraddr, temp)
        else:
            pass
            # print(smt)

    def init(self, needReg, needpc):
        self.func[-1].append(f"\taddi\tsp, sp, -{needpc * 4}\n")
        self.Reg.Unused.clear()
        self.Reg.Vars2Reg.clear()
        self.Reg.Vars2addr.clear()
        for i in range(needpc - 1, -1, -1):
            self.Reg.Unused.append(i * 4)

    def write(self):
        self.output.write('\t.text\n')
        for func in self.func:
            for str in func:
                self.output.write(str)
        self.output.write('\t.data\n')
        for var in self.globalvar:
            for str in var:
                self.output.write(str)
        self.output.flush()

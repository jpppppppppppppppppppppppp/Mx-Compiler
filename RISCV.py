import copy

from main import llvmEnum

binaryopt = {'mul': 'mul', 'sdiv': 'div', 'add': 'add', 'sub': 'sub', 'srem': 'rem', 'shl': 'sll', 'ashr': 'sra', 'and': 'and', 'or': 'or', 'xor': 'xor'}


class Regtrival:
    def __init__(self):
        self.Vars2addr = {}
        self.Vars2Reg = {}
        self.Unused = []
        self.Regtouse = ['t1', 't2', 't3']
        self.pc = 0
        self.ra = 0
        self.used = []

    def alloca(self, varname):
        if varname not in self.Vars2addr and len(self.Unused) > 0:
            addr = self.Unused.pop(0)
            self.Vars2addr[varname] = addr
        else:
            raise Exception("Warning")

    def var2Reg(self, array, var):
        if var.isdigit() or var[1:].isdigit():
            reg = self.Regtouse.pop(0)
            array.append(f'\tli\t{reg}, {var}\n')
            return reg, [reg]
        elif var[0] == '%':
            if var in self.Vars2Reg:
                return self.Vars2Reg[var], []
            else:
                addr, _ = self.var2Addr(array, var)
                reg = self.Regtouse.pop(0)
                array.append(f'\tlw\t{reg}, {addr}\n')
                return reg, [reg]
        elif var[0] == '@':
            reg = self.Regtouse.pop(0)
            array.append(f'\tlui\t{reg}, %hi({var[1:]})\n')
            array.append(f'\taddi\t{reg}, {reg}, %lo({var[1:]})\n')
            return reg, [reg]
        elif var == 'null':
            return 'x0', []
        elif var == 'true':
            reg = self.Regtouse.pop(0)
            array.append(f'\tli\t{reg}, 1\n')
            return reg, [reg]
        elif var == 'false':
            reg = self.Regtouse.pop(0)
            array.append(f'\tli\t{reg}, 0\n')
            return reg, [reg]
        else:
            raise Exception("Warning")
        return None, []

    def var2varReg(self, array, var):
        if var.isdigit() or var[1:].isdigit():
            reg = self.Regtouse.pop(0)
            array.append(f'\tli\t{reg}, {var}\n')
            return reg, [reg]
        elif var[0] == '%':
            if var in self.Vars2Reg:
                return self.Vars2Reg[var], []
            else:
                addr, _ = self.var2Addr(array, var)
                reg = self.Regtouse.pop(0)
                array.append(f'\tlw\t{reg}, {addr}\n')
                return reg, [reg]
        elif var[0] == '@':
            reg = self.Regtouse.pop(0)
            array.append(f'\tlui\t{reg}, %hi({var[1:]})\n')
            array.append(f'\tlw\t{reg}, %lo({var[1:]})({reg})\n')
            return reg, [reg]
        elif var == 'null':
            return 'x0', []
        elif var == 'true':
            reg = self.Regtouse.pop(0)
            array.append(f'\tli\t{reg}, 1\n')
            return reg, [reg]
        elif var == 'false':
            reg = self.Regtouse.pop(0)
            array.append(f'\tli\t{reg}, 0\n')
            return reg, [reg]
        else:
            raise Exception("Warning")
        return None, []

    def var2Addr(self, array, tar):
        if tar[0] == '%':
            if tar in self.Vars2addr:
                if type(self.Vars2addr[tar]).__name__ == 'int':
                    return str(self.Vars2addr[tar] + self.pc) + '(sp)', []
                else:
                    return self.Vars2addr[tar], []
            else:
                raise Exception("Warning")
        elif tar[0] == '@':
            reg = self.Regtouse.pop(0)
            array.append(f'\tlui\t{reg}, %hi({tar[1:]})\n')
            return f"%lo({tar[1:]})({reg})", [reg]
        else:
            print('addr', tar)
        return None, []

    def store(self, array, reg, addr, clean):
        array.append(f"\tsw\t{reg}, {addr}\n")
        for toclean in clean:
            self.Regtouse.append(toclean)
        for toclean in self.used:
            self.Regtouse.append(toclean)
        self.used.clear()

    def load(self, array, var, reg):
        if var.isdigit() or var[1:].isdigit():
            if reg.isdigit():
                array.append(f'\tli\t{self.Regtouse[0]}, {var}\n')
                array.append(f'\tsw\t{self.Regtouse[0]}, {reg}(sp)\n')
            else:
                array.append(f'\tli\t{reg}, {var}\n')
        elif var[0] == '%':
            if reg.isdigit():
                if var in self.Vars2Reg:
                    array.append(f'\tmv\t{self.Regtouse[0]}, {self.Vars2Reg[var]}\n')
                else:
                    addr, _ = self.var2Addr(array, var)
                    array.append(f'\tlw\t{self.Regtouse[0]}, {addr}\n')
                array.append(f'\tsw\t{self.Regtouse[0]}, {reg}(sp)\n')
            else:
                if var in self.Vars2Reg:
                    array.append(f'\tmv\t{reg}, {self.Vars2Reg[var]}\n')
                else:
                    addr, _ = self.var2Addr(array, var)
                    array.append(f'\tlw\t{reg}, {addr}\n')
        elif var[0] == '@':
            if reg.isdigit():
                array.append(f'\tlui\t{self.Regtouse[0]}, %hi({var[1:]})\n')
                array.append(f'\taddi\t{self.Regtouse[0]}, {self.Regtouse[0]}, %lo({var[1:]})\n')
                array.append(f'\tsw\t{self.Regtouse[0]}, {reg}(sp)\n')
            else:
                array.append(f'\tlui\t{reg}, %hi({var[1:]})\n')
                array.append(f'\taddi\t{reg}, {reg}, %lo({var[1:]})\n')
        else:
            raise Exception("Warning")

    def binary(self, array, op, lhs, rhs):
        reg = self.Regtouse.pop(0)
        array.append(f'\t{binaryopt[op]}\t{reg}, {lhs}, {rhs}\n')
        return reg, [reg]

    def GEP1(self, array, target, index, ans, clean):
        array.append(f"\tslli\t{index}, {index}, 2\n")
        array.append(f"\tadd\ts1, {target}, {index}\n")
        self.Vars2addr[ans] = f'0(s1)'
        for toclean in clean:
            self.Regtouse.append(toclean)

    def Icmp(self, array, op, lhs, rhs, ans, clean):
        reg = self.Regtouse[0]
        if op == 'eq':
            array.append(f"\txor\t{reg}, {lhs}, {rhs}\n")
            array.append(f"\tseqz\t{reg}, {reg}\n")
        elif op == 'ne':
            array.append(f"\txor\t{reg}, {lhs}, {rhs}\n")
            array.append(f"\tsnez\t{reg}, {reg}\n")
        elif op == 'slt':
            array.append(f"\tslt\t{reg}, {lhs}, {rhs}\n")
        elif op == 'sgt':
            array.append(f"\tslt\t{reg}, {rhs}, {lhs}\n")
        elif op == 'sle':
            array.append(f"\tslt\t{reg}, {rhs}, {lhs}\n")
            array.append(f"\txori\t{reg}, {reg}, 1\n")
        elif op == 'sge':
            array.append(f"\tslt\t{reg}, {lhs}, {rhs}\n")
            array.append(f"\txori\t{reg}, {reg}, 1\n")
        else:
            raise Exception("Warning")
        self.store(array, reg, ans, clean)

    def copy(self, array, target, var, clean):
        reg = self.Regtouse[0]
        array.append(f"\tandi\t{reg}, {var}, 1\n")
        self.store(array, reg, target, clean)


class RISCV:
    def __init__(self, filename):
        self.output = open(filename, 'w')
        self.Reg = Regtrival()
        self.globalvar = []
        self.func = []
        self.end = False
        self.pc = 0
        self.Maxarg = 0
        self.funcname = ''
        self.label = ''
        self.phi = {}
        self.phiaddr = {}

    def translateglobalvars(self, array):
        if array[0] == llvmEnum.GlobalVar:
            self.globalvar.append([])
            if type(array[3]).__name__ == 'str' and array[3][0] == '@':
                self.globalvar[-1].append(f'.{array[1]}:\n')
                self.globalvar[-1].append(f'\t.word {array[3][1:]}\n')
            elif array[3] == 'null':
                self.globalvar[-1].append(f'.{array[1]}:\n')
                self.globalvar[-1].append(f'\t.word 0\n')
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
        self.phi.clear()
        self.phiaddr.clear()
        self.funcname = funcname
        if funcname != 'main':
            varReg = {}
            varAddr = {}
            for i in range(len(array[1])):
                if i < 8:
                    varReg[array[1][i][1]] = f'a{i}'
                else:
                    varAddr[array[1][i][1]] = 4 * (i - 8)
            needpc = array[3] + self.Maxarg + len(array[1]) + 3
        else:
            varReg = {}
            varAddr = {}
            needpc = array[3] + self.Maxarg + len(array[1]) + 3
        for block in array[2]:
            if block[1][0] == llvmEnum.Phi:
                needpc += 1
                self.phi[block[0][1]] = {block[1][4]: block[1][3], block[1][6]: block[1][5]}
        self.func.append([f"\t.globl {funcname}\n", f"{funcname}:\t\t# @{funcname}\n"])
        self.init(varReg, varAddr, (needpc + 3) & ~3)
        for block in array[2]:
            self.translateblock(block)

    def translateblock(self, array):
        self.end = False
        for smt in array:
            self.translatesmt(smt)

    def translatesmt(self, smt):
        if self.end:
            return
        if smt[0] == llvmEnum.Label:
            self.label = smt[1]
            self.func[-1].append(f".{self.funcname}.{smt[1]}:\t\t# %{smt[1]}\n")
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
        elif smt[0] == llvmEnum.Load:
            temp = []
            self.Reg.alloca(smt[1])
            varReg, clean = self.Reg.var2varReg(self.func[-1], smt[3])
            for toclear in clean:
                temp.append(toclear)
            taraddr, clean = self.Reg.var2Addr(self.func[-1], smt[1])
            for toclear in clean:
                temp.append(toclear)
            self.Reg.store(self.func[-1], varReg, taraddr, temp)
        elif smt[0] == llvmEnum.Jump:
            if smt[1] in self.phi and self.label in self.phi[smt[1]]:
                temp = []
                varReg, clean = self.Reg.var2Reg(self.func[-1], self.phi[smt[1]][self.label])
                for toclear in clean:
                    temp.append(toclear)
                if smt[1] not in self.phiaddr:
                    self.phiaddr[smt[1]] = str(self.Reg.Unused.pop(0) + self.pc) + '(sp)'
                taraddr = self.phiaddr[smt[1]]
                self.Reg.store(self.func[-1], varReg, taraddr, temp)
            self.func[-1].append(f"\tj\t.{self.funcname}.{smt[1]}\n")
            self.end = True
        elif smt[0] == llvmEnum.Return:
            self.Reg.load(self.func[-1], smt[2], 'a0')
            self.func[-1].append(f"\tlw\tra, {self.ra}(sp)\n")
            self.func[-1].append(f"\taddi\tsp, sp, {self.pc}\n")
            self.func[-1].append("\tret\n")
            self.end = True
        elif smt[0] == llvmEnum.FuncCall:
            for i in range(len(smt[4])):
                if i < 8:
                    self.Reg.load(self.func[-1], smt[4][i][1], f'a{i}')
                else:
                    self.Reg.load(self.func[-1], smt[4][i][1], str((i - 8) * 4))
            self.func[-1].append(f"\tcall\t{smt[3]}\n")
            self.Reg.alloca(smt[1])
            self.Reg.store(self.func[-1], 'a0', self.Reg.var2Addr(self.func[-1], smt[1])[0], [])
        elif smt[0] == llvmEnum.FuncVoid:
            for i in range(len(smt[2])):
                if i < 8:
                    self.Reg.load(self.func[-1], smt[2][i][1], f'a{i}')
                else:
                    self.Reg.load(self.func[-1], smt[2][i][1], str((i - 8) * 4))
            self.func[-1].append(f"\tcall\t{smt[1]}\n")
        elif smt[0] == llvmEnum.Binary:
            self.Reg.alloca(smt[1])
            temp = []
            varReg1, clean = self.Reg.var2Reg(self.func[-1], smt[4])
            for toclear in clean:
                temp.append(toclear)
            varReg2, clean = self.Reg.var2Reg(self.func[-1], smt[5])
            for toclear in clean:
                temp.append(toclear)
            ansReg, clean = self.Reg.binary(self.func[-1], smt[2], varReg1, varReg2)
            for toclear in clean:
                temp.append(toclear)
            taraddr, clean = self.Reg.var2Addr(self.func[-1], smt[1])
            for toclear in clean:
                temp.append(toclear)
            self.Reg.store(self.func[-1], ansReg, taraddr, temp)
        elif smt[0] == llvmEnum.ReturnVoid:
            self.func[-1].append(f"\tlw\tra, {self.ra}(sp)\n")
            self.func[-1].append(f"\taddi\tsp, sp, {self.pc}\n")
            self.func[-1].append("\tret\n")
            self.end = True
        elif smt[0] == llvmEnum.Getelementptr1:
            temp = []
            tarReg, clean = self.Reg.var2Reg(self.func[-1], smt[3])
            for toclear in clean:
                temp.append(toclear)
            indReg, clean = self.Reg.var2Reg(self.func[-1], smt[4])
            for toclear in clean:
                temp.append(toclear)
            self.Reg.GEP1(self.func[-1], tarReg, indReg, smt[1], temp)
        elif smt[0] == llvmEnum.Getelementptr2:
            temp = []
            tarReg, clean = self.Reg.var2Reg(self.func[-1], smt[3])
            for toclear in clean:
                temp.append(toclear)
            indReg, clean = self.Reg.var2Reg(self.func[-1], smt[4])
            for toclear in clean:
                temp.append(toclear)
            self.Reg.GEP1(self.func[-1], tarReg, indReg, smt[1], temp)
        elif smt[0] == llvmEnum.Icmp:
            temp = []
            varReg1, clean = self.Reg.var2Reg(self.func[-1], smt[4])
            for toclear in clean:
                temp.append(toclear)
            varReg2, clean = self.Reg.var2Reg(self.func[-1], smt[5])
            for toclear in clean:
                temp.append(toclear)
            self.Reg.alloca(smt[1])
            self.Reg.Icmp(self.func[-1], smt[2], varReg1, varReg2, self.Reg.var2Addr(self.func[-1], smt[1])[0], temp)
        elif smt[0] == llvmEnum.Zext:
            temp = []
            varReg, clean = self.Reg.var2Reg(self.func[-1], smt[2])
            for toclear in clean:
                temp.append(toclear)
            self.Reg.alloca(smt[1])
            self.Reg.copy(self.func[-1], self.Reg.var2Addr(self.func[-1], smt[1])[0], varReg, temp)
        elif smt[0] == llvmEnum.Trunc:
            temp = []
            varReg, clean = self.Reg.var2Reg(self.func[-1], smt[2])
            for toclear in clean:
                temp.append(toclear)
            self.Reg.alloca(smt[1])
            self.Reg.copy(self.func[-1], self.Reg.var2Addr(self.func[-1], smt[1])[0], varReg, temp)
        elif smt[0] == llvmEnum.Br:
            temp = []
            if smt[2] in self.phi and self.label in self.phi[smt[2]]:
                temp = []
                varReg, clean = self.Reg.var2Reg(self.func[-1], self.phi[smt[2]][self.label])
                for toclear in clean:
                    temp.append(toclear)
                if smt[2] not in self.phiaddr:
                    self.phiaddr[smt[2]] = str(self.Reg.Unused.pop(0) + self.pc) + '(sp)'
                taraddr = self.phiaddr[smt[2]]
                self.Reg.store(self.func[-1], varReg, taraddr, temp)
            temp.clear()
            conReg, clean = self.Reg.var2Reg(self.func[-1], smt[1])
            for toclear in clean:
                temp.append(toclear)
            self.func[-1].append(f'\tbnez\t{conReg}, .{self.funcname}.{smt[2]}\n')
            for toclean in temp:
                self.Reg.Regtouse.append(toclean)
            temp.clear()
            if smt[3] in self.phi and self.label in self.phi[smt[3]]:
                temp = []
                varReg, clean = self.Reg.var2Reg(self.func[-1], self.phi[smt[3]][self.label])
                for toclear in clean:
                    temp.append(toclear)
                if smt[3] not in self.phiaddr:
                    self.phiaddr[smt[3]] = str(self.Reg.Unused.pop(0) + self.pc) + '(sp)'
                taraddr = self.phiaddr[smt[3]]
                self.Reg.store(self.func[-1], varReg, taraddr, temp)
            self.func[-1].append(f'\tj\t.{self.funcname}.{smt[3]}\n')
            self.end = True
        elif smt[0] == llvmEnum.Phi:
            self.Reg.alloca(smt[1])
            if self.label not in self.phiaddr:
                self.phiaddr[self.label] = str(self.Reg.Unused.pop(0) + self.pc) + '(sp)'
            taraddr = self.phiaddr[self.label]
            reg = self.Reg.Regtouse[0]
            self.func[-1].append(f"\tlw\t{reg}, {taraddr}\n")
            self.Reg.store(self.func[-1], reg, self.Reg.var2Addr(self.func[-1], smt[1])[0], [])
        else:
            print(smt)

    def init(self, needReg, needAddr, needpc):
        self.func[-1].append(f"\taddi\tsp, sp, -{needpc * 4}\n")
        self.Reg.Unused.clear()
        self.Reg.used.clear()
        self.Reg.Vars2Reg.clear()
        self.Reg.Vars2addr.clear()
        self.pc = 4 * needpc
        self.Reg.pc = 4 * needpc
        for i in range(1, needpc + 1):
            self.Reg.Unused.append(-i * 4)
        self.ra = self.Reg.Unused.pop(0) + self.pc
        self.func[-1].append(f"\tsw\tra, {self.ra}(sp)\n")
        for var in needReg:
            self.Reg.Vars2Reg[var] = needReg[var]
        for var in needAddr:
            self.Reg.Vars2addr[var] = needAddr[var]

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

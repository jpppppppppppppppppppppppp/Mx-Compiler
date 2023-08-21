from llvmEnum import *


class regalloc:
    def __init__(self):
        pass

    def translate(self, globalvars, allfunc):
        for function in allfunc:
            self.staticAnalyze(allfunc[function])

    def staticAnalyze(self, function):
        pre = {}
        next = {}
        defd = {}
        used = {}
        phi = {}
        alldefd = {}
        allused = {}
        nowlabel = ""
        for label in function[2]:
            for smt in label:
                if smt[0] == llvmEnum.Label:
                    nowlabel = smt[1]
                elif smt[0] == llvmEnum.Phi:
                    for sub in smt[3]:
                        if sub[1] not in phi:
                            phi[sub[1]] = {}
                        phi[sub[1]][smt[1]] = sub[0]
        for label in function[2]:
            for smt in label:
                if smt[0] == llvmEnum.Label:
                    nowlabel = smt[1]
                    if nowlabel not in pre:
                        pre[nowlabel] = set()
                    if nowlabel not in next:
                        next[nowlabel] = set()
                    defd[nowlabel] = set()
                    used[nowlabel] = set()
                    alldefd[nowlabel] = set()
                    allused[nowlabel] = set()
                elif smt[0] == llvmEnum.Alloca:
                    alldefd[nowlabel].add(smt[1])
                    defd[nowlabel].add(smt[1])
                elif smt[0] == llvmEnum.Load:
                    alldefd[nowlabel].add(smt[1])
                    defd[nowlabel].add(smt[1])
                    if smt[3] not in alldefd[nowlabel]:
                        used[nowlabel].add(smt[3])
                    allused[nowlabel].add(smt[3])
                elif smt[0] == llvmEnum.Return:
                    if smt[2][0] in ['%', '@']:
                        if smt[2] not in alldefd[nowlabel]:
                            used[nowlabel].add(smt[2])
                        allused[nowlabel].add(smt[2])
                elif smt[0] == llvmEnum.Getelementptr1:
                    alldefd[nowlabel].add(smt[1])
                    defd[nowlabel].add(smt[1])
                    if smt[3] not in alldefd[nowlabel]:
                        used[nowlabel].add(smt[3])
                    allused[nowlabel].add(smt[3])
                    if smt[4][0] in ['%', '@']:
                        if smt[4] not in alldefd[nowlabel]:
                            used[nowlabel].add(smt[4])
                        allused[nowlabel].add(smt[4])
                elif smt[0] == llvmEnum.Getelementptr2:
                    alldefd[nowlabel].add(smt[1])
                    defd[nowlabel].add(smt[1])
                    if smt[3] not in alldefd[nowlabel]:
                        used[nowlabel].add(smt[3])
                    allused[nowlabel].add(smt[3])
                    if smt[4][0] in ['%', '@']:
                        if smt[4] not in alldefd[nowlabel]:
                            used[nowlabel].add(smt[4])
                        allused[nowlabel].add(smt[4])
                elif smt[0] == llvmEnum.Jump:
                    if nowlabel in phi:
                        for var in phi[nowlabel]:
                            if var not in allused[nowlabel]:
                                defd[nowlabel].add(var)
                            alldefd[nowlabel].add(var)
                            if phi[nowlabel][var][0] in ['%', '@']:
                                if phi[nowlabel][var][0] not in alldefd[nowlabel]:
                                    used[nowlabel].add(phi[nowlabel][var][0])
                                allused[nowlabel].add(phi[nowlabel][var][0])
                    next[nowlabel].add(smt[1])
                    if smt[1] not in pre:
                        pre[smt[1]] = set()
                    pre[smt[1]].add(nowlabel)
                elif smt[0] == llvmEnum.Trunc:
                    alldefd[nowlabel].add(smt[1])
                    defd[nowlabel].add(smt[1])
                    if smt[2][0] in ['%', '@']:
                        if smt[2] not in alldefd[nowlabel]:
                            used[nowlabel].add(smt[2])
                        allused[nowlabel].add(smt[2])
                elif smt[0] == llvmEnum.Br:
                    if nowlabel in phi:
                        for var in phi[nowlabel]:
                            if var not in allused[nowlabel]:
                                defd[nowlabel].add(var)
                            alldefd[nowlabel].add(var)
                            if phi[nowlabel][var][0] in ['%', '@']:
                                if phi[nowlabel][var][0] not in alldefd[nowlabel]:
                                    used[nowlabel].add(phi[nowlabel][var][0])
                                allused[nowlabel].add(phi[nowlabel][var][0])
                    if smt[1][0] in ['%', '@']:
                        if smt[1] not in alldefd[nowlabel]:
                            used[nowlabel].add(smt[1])
                        allused[nowlabel].add(smt[1])
                    next[nowlabel].add(smt[2])
                    next[nowlabel].add(smt[3])
                    if smt[2] not in pre:
                        pre[smt[2]] = set()
                    pre[smt[2]].add(nowlabel)
                    if smt[3] not in pre:
                        pre[smt[3]] = set()
                    pre[smt[3]].add(nowlabel)
                elif smt[0] == llvmEnum.Zext:
                    alldefd[nowlabel].add(smt[1])
                    defd[nowlabel].add(smt[1])
                    if smt[2][0] in ['%', '@']:
                        if smt[2] not in alldefd[nowlabel]:
                            used[nowlabel].add(smt[2])
                        allused[nowlabel].add(smt[2])
                elif smt[0] == llvmEnum.Icmp:
                    alldefd[nowlabel].add(smt[1])
                    defd[nowlabel].add(smt[1])
                    if smt[4][0] in ['%', '@']:
                        if smt[4] not in alldefd[nowlabel]:
                            used[nowlabel].add(smt[4])
                        allused[nowlabel].add(smt[4])
                    if smt[5][0] in ['%', '@']:
                        if smt[5] not in alldefd[nowlabel]:
                            used[nowlabel].add(smt[5])
                        allused[nowlabel].add(smt[5])
                elif smt[0] == llvmEnum.Store:
                    if smt[2][0] in ['%', '@']:
                        if smt[2] not in alldefd[nowlabel]:
                            used[nowlabel].add(smt[2])
                        allused[nowlabel].add(smt[2])
                    if smt[3] not in allused[nowlabel]:
                        defd[nowlabel].add(smt[3])
                    alldefd[nowlabel].add(smt[3])
                elif smt[0] == llvmEnum.Binary:
                    alldefd[nowlabel].add(smt[1])
                    defd[nowlabel].add(smt[1])
                    if smt[4][0] in ['%', '@']:
                        if smt[4] not in alldefd[nowlabel]:
                            used[nowlabel].add(smt[4])
                        allused[nowlabel].add(smt[4])
                    if smt[5][0] in ['%', '@']:
                        if smt[5] not in alldefd[nowlabel]:
                            used[nowlabel].add(smt[5])
                        allused[nowlabel].add(smt[5])
                elif smt[0] == llvmEnum.FuncCall:
                    alldefd[nowlabel].add(smt[1])
                    defd[nowlabel].add(smt[1])
                    for arg in smt[4]:
                        if arg[1][0] in ['%', '@']:
                            if arg[1] not in alldefd[nowlabel]:
                                used[nowlabel].add(arg[1])
                            allused[nowlabel].add(arg[1])
                elif smt[0] == llvmEnum.FuncVoid:
                    for arg in smt[2]:
                        if arg[1][0] in ['%', '@']:
                            if arg[1] not in alldefd[nowlabel]:
                                used[nowlabel].add(arg[1])
                            allused[nowlabel].add(arg[1])
        print(phi)
        print(defd)
        print(used)

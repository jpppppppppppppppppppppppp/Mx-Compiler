from classEnum import *

reg2use = ['a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 't0', 't1', 't2', 't3', 't4', 't5', 't6', 's0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9',
           's10', 's11']
caller = ['a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 't0', 't1', 't2', 't3', 't4', 't5', 't6']

binaryopt = {'mul': 'mul', 'sdiv': 'div', 'add': 'add', 'sub': 'sub', 'srem': 'rem', 'shl': 'sll', 'ashr': 'sra', 'and': 'and', 'or': 'or', 'xor': 'xor'}


class regalloc:
    def __init__(self):
        self.varnum = 0

    def translate(self, globalvars, allfunc):
        ir = {}
        for function in allfunc:
            ir[function] = self.make(allfunc[function])

    def staticAnalyze(self, function):
        pre = {}
        next = {}
        defd = {}
        used = {}
        phi = {}
        alldefd = {}
        allused = {}
        nowlabel = ""
        alllabel = {}
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
                    alllabel[nowlabel] = label
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
                    if smt[3][0] == '@':
                        if smt[3] not in allused[nowlabel]:
                            defd[nowlabel].add(smt[3])
                        alldefd[nowlabel].add(smt[3])
                    if smt[3] not in alldefd[nowlabel]:
                        used[nowlabel].add(smt[3])
                    allused[nowlabel].add(smt[3])
                elif smt[0] == llvmEnum.Return:
                    if smt[2][0] in ['%', '@']:
                        if smt[2][0] == '@':
                            if smt[2] not in allused[nowlabel]:
                                defd[nowlabel].add(smt[2])
                            alldefd[nowlabel].add(smt[2])
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
                                if phi[nowlabel][var] not in alldefd[nowlabel]:
                                    used[nowlabel].add(phi[nowlabel][var])
                                allused[nowlabel].add(phi[nowlabel][var])
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
                                if phi[nowlabel][var] not in alldefd[nowlabel]:
                                    used[nowlabel].add(phi[nowlabel][var])
                                allused[nowlabel].add(phi[nowlabel][var])
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
                        if smt[2][0] == '@':
                            if smt[2] not in allused[nowlabel]:
                                defd[nowlabel].add(smt[2])
                            alldefd[nowlabel].add(smt[2])
                        if smt[2] not in alldefd[nowlabel]:
                            used[nowlabel].add(smt[2])
                        allused[nowlabel].add(smt[2])
                    if smt[3][0] == '@':
                        if smt[3] not in allused[nowlabel]:
                            defd[nowlabel].add(smt[3])
                        alldefd[nowlabel].add(smt[3])
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
                            if arg[1][0] == '@':
                                if arg[1] not in allused[nowlabel]:
                                    defd[nowlabel].add(arg[1])
                                alldefd[nowlabel].add(arg[1])
                            if arg[1] not in alldefd[nowlabel]:
                                used[nowlabel].add(arg[1])
                            allused[nowlabel].add(arg[1])
                elif smt[0] == llvmEnum.FuncVoid:
                    for arg in smt[2]:
                        if arg[1][0] in ['%', '@']:
                            if arg[1][0] == '@':
                                if arg[1] not in allused[nowlabel]:
                                    defd[nowlabel].add(arg[1])
                                alldefd[nowlabel].add(arg[1])
                            if arg[1] not in alldefd[nowlabel]:
                                used[nowlabel].add(arg[1])
                            allused[nowlabel].add(arg[1])
        allin = {}
        allout = {}
        for label in alllabel:
            if label not in allin:
                allin[label] = set()
            if label not in allout:
                allout[label] = set()
        while True:
            update = False
            for label in alllabel:
                newout = set()
                for suc in next[label]:
                    newout = newout.union(allin[suc])
                if not newout == allout[label]:
                    update = True
                    allout[label] = newout
                newin = used[label].union(allout[label] - defd[label])
                if not newin == allin[label]:
                    update = True
                    allin[label] = newin
            if not update:
                break
        liveout = {}
        for label in alllabel:
            liveout[label] = [set() for _ in range(len(alllabel[label]))]
            begin = True
            nextind = 0
            for i in range(len(alllabel[label]) - 1, 0, -1):
                smt = alllabel[label][i]
                if smt[0] == llvmEnum.Pass or smt[0] == llvmEnum.Phi:
                    continue
                if begin:
                    begin = False
                    nextind = i
                    liveout[label][i] = allout[label]
                    continue
                smt = alllabel[label][nextind]
                if smt[0] == llvmEnum.Alloca:
                    liveout[label][i] = liveout[label][nextind].copy()
                    nextind = i
                    liveout[label][i].discard(smt[1])
                elif smt[0] == llvmEnum.Load:
                    liveout[label][i] = liveout[label][nextind].copy()
                    nextind = i
                    liveout[label][i].discard(smt[1])
                    liveout[label][i].add(smt[3])
                    if smt[3][0] == '@':
                        liveout[label][i].discard(smt[3])
                elif smt[0] == llvmEnum.Return:
                    liveout[label][i] = liveout[label][nextind].copy()
                    nextind = i
                    if smt[2][0] in ['%', '@']:
                        liveout[label][i].add(smt[2])
                        if smt[2][0] == '@':
                            liveout[label][i].discard(smt[2])
                elif smt[0] == llvmEnum.Getelementptr1:
                    liveout[label][i] = liveout[label][nextind].copy()
                    nextind = i
                    liveout[label][i].discard(smt[1])
                    if smt[3][0] in ['%', '@']:
                        liveout[label][i].add(smt[3])
                    if smt[4][0] in ['%', '@']:
                        liveout[label][i].add(smt[4])
                elif smt[0] == llvmEnum.Getelementptr2:
                    liveout[label][i] = liveout[label][nextind].copy()
                    nextind = i
                    liveout[label][i].discard(smt[1])
                    if smt[3][0] in ['%', '@']:
                        liveout[label][i].add(smt[3])
                    if smt[4][0] in ['%', '@']:
                        liveout[label][i].add(smt[4])
                elif smt[0] == llvmEnum.Jump:
                    liveout[label][i] = liveout[label][nextind].copy()
                    nextind = i
                    if label in phi:
                        for var in phi[label]:
                            liveout[label][i].discard(var)
                            if phi[label][var][0] in ['%', '@']:
                                liveout[label][i].add(phi[label][var])
                elif smt[0] == llvmEnum.Trunc:
                    liveout[label][i] = liveout[label][nextind].copy()
                    nextind = i
                    liveout[label][i].discard(smt[1])
                    if smt[2][0] in ['%', '@']:
                        liveout[label][i].add(smt[2])
                elif smt[0] == llvmEnum.Br:
                    liveout[label][i] = liveout[label][nextind].copy()
                    nextind = i
                    if smt[1][0] in ['%', '@']:
                        liveout[label][i].add(smt[1])
                    if label in phi:
                        for var in phi[label]:
                            liveout[label][i].discard(var)
                            if phi[label][var][0] in ['%', '@']:
                                liveout[label][i].add(phi[label][var])
                elif smt[0] == llvmEnum.Zext:
                    liveout[label][i] = liveout[label][nextind].copy()
                    nextind = i
                    liveout[label][i].discard(smt[1])
                    if smt[2][0] in ['%', '@']:
                        liveout[label][i].add(smt[2])
                elif smt[0] == llvmEnum.Icmp:
                    liveout[label][i] = liveout[label][nextind].copy()
                    nextind = i
                    liveout[label][i].discard(smt[1])
                    if smt[4][0] in ['%', '@']:
                        liveout[label][i].add(smt[4])
                    if smt[5][0] in ['%', '@']:
                        liveout[label][i].add(smt[5])
                elif smt[0] == llvmEnum.Store:
                    liveout[label][i] = liveout[label][nextind].copy()
                    nextind = i
                    liveout[label][i].discard(smt[3])
                    if smt[2][0] in ['%', '@']:
                        liveout[label][i].add(smt[2])
                        if smt[2][0] == '@':
                            liveout[label][i].discard(smt[2])
                elif smt[0] == llvmEnum.Binary:
                    liveout[label][i] = liveout[label][nextind].copy()
                    nextind = i
                    liveout[label][i].discard(smt[1])
                    if smt[4][0] in ['%', '@']:
                        liveout[label][i].add(smt[4])
                    if smt[5][0] in ['%', '@']:
                        liveout[label][i].add(smt[5])
                elif smt[0] == llvmEnum.FuncCall:
                    liveout[label][i] = liveout[label][nextind].copy()
                    nextind = i
                    liveout[label][i].discard(smt[1])
                    for arg in smt[4]:
                        if arg[1][0] in ['%', '@']:
                            liveout[label][i].add(arg[1])
                            if arg[1][0] == '@':
                                liveout[label][i].discard(arg[1])
                elif smt[0] == llvmEnum.FuncVoid:
                    liveout[label][i] = liveout[label][nextind].copy()
                    nextind = i
                    for arg in smt[2]:
                        if arg[1][0] in ['%', '@']:
                            liveout[label][i].add(arg[1])
                            liveout[label][i].add(arg[1])
                            if arg[1][0] == '@':
                                liveout[label][i].discard(arg[1])
                elif smt[0] == llvmEnum.ReturnVoid:
                    liveout[label][i] = liveout[label][nextind].copy()
                    nextind = i
        edges = {}
        confivar = {}
        varsinstack = {}
        for label in alllabel:
            if label == 'entry':
                temp = allin[label].copy()
                for j in range(len(function[1]) - 1, -1, -1):
                    arg = function[1][j][1]
                    if arg not in edges:
                        edges[arg] = set()
                    for var in temp:
                        if var not in edges:
                            edges[var] = set()
                        edges[arg].add(var)
                        edges[var].add(arg)
                    temp.discard(arg)
            for i in range(len(alllabel[label])):
                smt = alllabel[label][i]
                if smt[0] == llvmEnum.Alloca:
                    if smt[1] not in edges:
                        edges[smt[1]] = set()
                    for cri in liveout[label][i]:
                        if cri not in edges:
                            edges[cri] = set()
                        edges[smt[1]].add(cri)
                        edges[cri].add(smt[1])
                elif smt[0] == llvmEnum.Load:
                    if smt[1] not in edges:
                        edges[smt[1]] = set()
                    for cri in liveout[label][i]:
                        if cri not in edges:
                            edges[cri] = set()
                        edges[smt[1]].add(cri)
                        edges[cri].add(smt[1])
                    if smt[2][0] == '@':
                        temp = liveout[label][i].copy()
                        temp.discard(smt[1])
                        temp.add(smt[2])
                        if smt[2] not in edges:
                            edges[smt[2]] = set()
                        for cri in temp:
                            if cri not in edges:
                                edges[cri] = set()
                            edges[smt[2]].add(cri)
                            edges[cri].add(smt[2])
                elif smt[0] == llvmEnum.Getelementptr1:
                    if smt[1] not in edges:
                        edges[smt[1]] = set()
                    for cri in liveout[label][i]:
                        if cri not in edges:
                            edges[cri] = set()
                        edges[smt[1]].add(cri)
                        edges[cri].add(smt[1])
                elif smt[0] == llvmEnum.Getelementptr2:
                    if smt[1] not in edges:
                        edges[smt[1]] = set()
                    for cri in liveout[label][i]:
                        if cri not in edges:
                            edges[cri] = set()
                        edges[smt[1]].add(cri)
                        edges[cri].add(smt[1])
                elif smt[0] == llvmEnum.Jump:
                    temp = liveout[label][i].copy()
                    if label in phi:
                        for var in phi[label]:
                            if var not in edges:
                                edges[var] = set()
                            for cri in temp:
                                if cri not in edges:
                                    edges[cri] = set()
                                edges[var].add(cri)
                                edges[cri].add(var)
                            temp.discard(var)
                            if phi[label][var][0] in ['%', '@']:
                                temp.add(phi[label][var])
                elif smt[0] == llvmEnum.Trunc:
                    if smt[1] not in edges:
                        edges[smt[1]] = set()
                    for cri in liveout[label][i]:
                        if cri not in edges:
                            edges[cri] = set()
                        edges[smt[1]].add(cri)
                        edges[cri].add(smt[1])
                elif smt[0] == llvmEnum.Br:
                    temp = liveout[label][i].copy()
                    if smt[1][0] in ['%', '@']:
                        temp.add(smt[1])
                    if label in phi:
                        for var in phi[label]:
                            if var not in edges:
                                edges[var] = set()
                            for cri in temp:
                                if cri not in edges:
                                    edges[cri] = set()
                                edges[var].add(cri)
                                edges[cri].add(var)
                            temp.discard(var)
                            if phi[label][var][0] in ['%', '@']:
                                temp.add(phi[label][var])
                elif smt[0] == llvmEnum.Zext:
                    if smt[1] not in edges:
                        edges[smt[1]] = set()
                    for cri in liveout[label][i]:
                        if cri not in edges:
                            edges[cri] = set()
                        edges[smt[1]].add(cri)
                        edges[cri].add(smt[1])
                elif smt[0] == llvmEnum.Icmp:
                    if smt[1] not in edges:
                        edges[smt[1]] = set()
                    for cri in liveout[label][i]:
                        if cri not in edges:
                            edges[cri] = set()
                        edges[smt[1]].add(cri)
                        edges[cri].add(smt[1])
                elif smt[0] == llvmEnum.Store:
                    if smt[3] not in edges:
                        edges[smt[3]] = set()
                    for cri in liveout[label][i]:
                        if cri not in edges:
                            edges[cri] = set()
                        edges[smt[3]].add(cri)
                        edges[cri].add(smt[3])
                    temp = liveout[label][i].copy()
                    temp.discard(smt[3])
                    temp.add(smt[2])
                    if smt[3][0] == '@':
                        if smt[3] not in edges:
                            edges[smt[3]] = set()
                        for cri in temp:
                            if cri not in edges:
                                edges[cri] = set()
                            edges[smt[3]].add(cri)
                            edges[cri].add(smt[3])
                        temp.discard(smt[3])
                    if smt[2][0] == '@':
                        if smt[2] not in edges:
                            edges[smt[2]] = set()
                        for cri in temp:
                            if cri not in edges:
                                edges[cri] = set()
                            edges[smt[2]].add(cri)
                            edges[cri].add(smt[2])
                        temp.discard(smt[2])
                elif smt[0] == llvmEnum.Binary:
                    if smt[1] not in edges:
                        edges[smt[1]] = set()
                    for cri in liveout[label][i]:
                        if cri not in edges:
                            edges[cri] = set()
                        edges[smt[1]].add(cri)
                        edges[cri].add(smt[1])
                elif smt[0] == llvmEnum.FuncCall:
                    if smt[1] not in edges:
                        edges[smt[1]] = set()
                    for cri in liveout[label][i]:
                        if cri not in edges:
                            edges[cri] = set()
                        edges[smt[1]].add(cri)
                        edges[cri].add(smt[1])
                    temp = liveout[label][i].copy()
                    temp.discard(smt[1])
                    todo = []
                    size = 0
                    for arg in smt[4]:
                        if arg[1][0] in ['%', '@']:
                            if size < 8:
                                confivar[arg[1]] = reg2use.index(f'a{size}')
                            temp.add(arg[1])
                            if arg[1][0] == '@':
                                if arg[1][0] not in todo:
                                    todo.append(arg[1])
                        size += 1
                    for arg in todo:
                        if arg not in edges:
                            edges[arg] = set()
                        for cri in temp:
                            if cri not in edges:
                                edges[cri] = set()
                            edges[arg].add(cri)
                            edges[cri].add(arg)
                        temp.discard(arg)
                elif smt[0] == llvmEnum.Return:
                    if smt[2][0] == '@':
                        confivar[smt[2]] = reg2use.index('a0')
                        temp = liveout[label][i].copy()
                        temp.add(smt[2])
                        if smt[2] not in edges:
                            edges[smt[2]] = set()
                        for cri in temp:
                            if cri not in edges:
                                edges[cri] = set()
                            edges[smt[2]].add(cri)
                            edges[cri].add(smt[2])
                elif smt[0] == llvmEnum.FuncVoid:
                    temp = liveout[label][i].copy()
                    todo = []
                    size = 0
                    for arg in smt[2]:
                        if arg[1][0] in ['%', '@']:
                            if size < 8:
                                confivar[arg[1]] = reg2use.index(f'a{size}')
                            temp.add(arg[1])
                            if arg[1][0] == '@':
                                if arg[1][0] not in todo:
                                    todo.append(arg[1])
                        size += 1
                    for arg in todo:
                        if arg not in edges:
                            edges[arg] = set()
                        for cri in temp:
                            if cri not in edges:
                                edges[cri] = set()
                            edges[arg].add(cri)
                            edges[cri].add(arg)
                        temp.discard(arg)
        print(allout)
        allvar = {}

    def make(self, array):
        varbank = {}
        tempconst = {}
        ret = []
        allblock = {'entry': [[lrEnum.label, 'entry']]}
        for i in range(len(array[1])):
            if i < 8:
                varname = f"temp_{self.varnum}"
                varbank[array[1][i][1]] = varname
                self.varnum += 1
                allblock['entry'].append([lrEnum.mv, varname, f'a{i}'])
            else:
                varname = f"temp_{self.varnum}"
                varbank[array[1][i][1]] = varname
                self.varnum += 1
                allblock['entry'].append([lrEnum.lw, varname, (i - 8) * 4, 'sp'])
        pre = {}
        next = {}
        phi = {}
        for label in array[2]:
            nowlabel = ""
            for smt in label:
                if smt[0] == llvmEnum.Label:
                    nowlabel = smt[1]
                    if nowlabel not in pre:
                        pre[nowlabel] = []
                    if nowlabel not in next:
                        next[nowlabel] = []
                elif smt[0] == llvmEnum.Br:
                    if nowlabel not in next:
                        next[nowlabel] = []
                    next[nowlabel].append(smt[2])
                    next[nowlabel].append(smt[3])
                    if smt[2] not in pre:
                        pre[smt[2]] = []
                    pre[smt[2]].append(nowlabel)
                    if smt[3] not in pre:
                        pre[smt[3]] = []
                    pre[smt[3]].append(nowlabel)
                elif smt[0] == llvmEnum.Jump:
                    if nowlabel not in next:
                        next[nowlabel] = []
                    next[nowlabel].append(smt[1])
                    if smt[1] not in pre:
                        pre[smt[1]] = []
                    pre[smt[1]].append(nowlabel)
                elif smt[0] == llvmEnum.Phi:
                    for arg in smt[3]:
                        if arg[1] not in phi:
                            phi[arg[1]] = {}
                        if nowlabel not in phi[arg[1]]:
                            phi[arg[1]][nowlabel] = []
                        phi[arg[1]][nowlabel].append([smt[1], arg[0]])
        for label in array[2]:
            nowlabel = ""
            for smt in label:
                if smt[0] == llvmEnum.Pass:
                    continue
                elif smt[0] == llvmEnum.Label:
                    nowlabel = smt[1]
                    if nowlabel not in allblock:
                        allblock[nowlabel] = [[lrEnum.label, nowlabel]]
                    ret.append(allblock[nowlabel])
                elif smt[0] == llvmEnum.Alloca:
                    raise Exception("No Alloca!")
                elif smt[0] == llvmEnum.Binary:
                    lhsvalue, lhscheck = self.constcheck(tempconst, smt[4])
                    rhsvalue, rhscheck = self.constcheck(tempconst, smt[5])
                    if lhscheck and rhscheck:
                        tempconst[smt[1]] = self.getvalue(smt[2], lhsvalue, rhsvalue)
                    else:
                        varname = f"temp_{self.varnum}"
                        self.varnum += 1
                        varbank[smt[1]] = varname
                        if lhscheck:
                            allblock[nowlabel].append([lrEnum.li, varname, lhsvalue])
                            allblock[nowlabel].append([lrEnum.binary, binaryopt[smt[2]], varname, varname, varbank[smt[5]]])
                        elif rhscheck:
                            allblock[nowlabel].append([lrEnum.binary, binaryopt[smt[2]] + 'i', varname, varbank[smt[4]], rhsvalue])
                        else:
                            allblock[nowlabel].append([lrEnum.binary, binaryopt[smt[2]], varname, varbank[smt[4]], varbank[smt[5]]])
                elif smt[0] == llvmEnum.Return:
                    if smt[2] in tempconst:
                        allblock[nowlabel].append([lrEnum.li, 'a0', tempconst[smt[2]]])
                    else:
                        allblock[nowlabel].append([lrEnum.mv, 'a0', varbank[smt[2]]])
                else:
                    print(smt)
        print(ret)
        return ret

    def constcheck(self, tempconst, var):
        if var.isdigit() or var[1:].isdigit():
            return int(var), True
        if var in tempconst:
            return tempconst[var], True
        return None, False

    def getvalue(self, op, lhs, rhs):
        if op == 'add':
            return lhs + rhs
        if op == 'sub':
            return lhs - rhs
        if op == 'mul':
            return lhs * rhs
        if op == 'sdiv':
            return lhs / rhs
        if op == 'srem':
            return lhs % rhs
        if op == 'shl':
            return lhs << rhs
        if op == 'ashr':
            return lhs >> rhs
        if op == 'and':
            return lhs & rhs
        if op == 'xor':
            return lhs ^ rhs
        if op == 'or':
            return lhs | rhs

from classEnum import *

reg2use = ['a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 't0', 't1', 't2', 't3', 't4', 't5', 't6', 's0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9',
           's10', 's11']
caller = ['a0', 'a1', 'a2', 'a3', 'a4', 'a5', 'a6', 'a7', 't0', 't1', 't2', 't3', 't4', 't5', 't6']
callee = ['s0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11']
binaryopt = {'mul': 'mul', 'sdiv': 'div', 'add': 'add', 'sub': 'sub', 'srem': 'rem', 'shl': 'sll', 'ashr': 'sra', 'and': 'and', 'or': 'or', 'xor': 'xor'}


class regalloc:
    def __init__(self):
        self.varnum = 0
        self.needra = False
        self.funcarg = 0
        self.spillnum = 0

    def mvrelated(self, name, movelist, activemMove, mvlib):
        if name not in movelist:
            return False
        for mv in movelist[name]:
            if mv in activemMove or mv in mvlib:
                return True
        return False

    def translate(self, globalvars, allfunc, dt):
        ir = {}
        output = open("test.s", 'w')
        output.write('\t.text\n')
        for function in allfunc:
            ir[function] = self.make(function, allfunc[function], dt[function])
            while True:
                mvlib, movelist, graph = self.staticAnalyze(ir[function])
                origingraph = {}
                for reg in graph:
                    origingraph[reg] = graph[reg].copy()
                selectStack = []
                coalescedNodes = {}
                coalescedMove = []
                constrainedMove = []
                frozenlist = []
                activemMove = []
                spillworklist, freezeworklist, simplifyworklist = self.makeworklist(mvlib, graph, movelist, activemMove)
                while not (len(simplifyworklist) == 0 and len(freezeworklist) == 0 and len(spillworklist) == 0 and len(mvlib) == 0):
                    if len(simplifyworklist) != 0:
                        self.simplify(simplifyworklist, selectStack, mvlib, movelist, graph, activemMove, coalescedNodes, spillworklist,
                                      freezeworklist)
                    elif len(mvlib) != 0:
                        self.coalesce(spillworklist, selectStack, mvlib, movelist, graph, activemMove, constrainedMove, coalescedMove,
                                      coalescedNodes, freezeworklist, simplifyworklist)
                    elif len(freezeworklist) != 0:
                        self.freeze(freezeworklist, simplifyworklist, movelist, mvlib, activemMove, coalescedNodes, frozenlist, graph)
                    elif len(spillworklist) != 0:
                        self.selectspill(spillworklist, simplifyworklist, movelist, activemMove, mvlib, coalescedNodes, frozenlist, graph, freezeworklist)
                coloredNode, spilledNode = self.Assigncolors(selectStack, graph, coalescedNodes)
                if len(spilledNode) != 0:
                    self.ReWrite(spilledNode, ir[function])
                    continue
                break
            for reg in reg2use:
                coloredNode[reg] = reg2use.index(reg)
            self.writefunction(output, function, ir[function], coloredNode, coalescedNodes)
        output.write('\t.data\n')
        for var in globalvars:
            self.writeglobalvar(output, var)
        output.flush()

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
        needra = False
        mvlib = []
        mvlist = {}
        for label in function:
            for smt in label:
                if smt[0] == lrEnum.label:
                    nowlabel = smt[2]
                    alllabel[nowlabel] = label
                    if nowlabel not in pre:
                        pre[nowlabel] = set()
                    if nowlabel not in next:
                        next[nowlabel] = set()
                    defd[nowlabel] = {'sp'}
                    used[nowlabel] = set()
                    alldefd[nowlabel] = {'sp'}
                    allused[nowlabel] = set()
                elif smt[0] == lrEnum.mv:
                    mvlib.append([smt[1], smt[2]])
                    if smt[1] not in mvlist:
                        mvlist[smt[1]] = []
                    mvlist[smt[1]].append([smt[1], smt[2]])
                    if smt[2] not in mvlist:
                        mvlist[smt[2]] = []
                    mvlist[smt[2]].append([smt[1], smt[2]])
                    if smt[2] not in alldefd[nowlabel]:
                        used[nowlabel].add(smt[2])
                    allused[nowlabel].add(smt[2])
                    if smt[1] not in allused[nowlabel]:
                        defd[nowlabel].add(smt[1])
                    alldefd[nowlabel].add(smt[1])
                elif smt[0] == lrEnum.lw:
                    if smt[3] not in alldefd[nowlabel]:
                        used[nowlabel].add(smt[3])
                    allused[nowlabel].add(smt[3])
                    if smt[1] not in allused[nowlabel]:
                        defd[nowlabel].add(smt[1])
                    alldefd[nowlabel].add(smt[1])
                elif smt[0] == lrEnum.binary:
                    if smt[3] not in alldefd[nowlabel]:
                        used[nowlabel].add(smt[3])
                    allused[nowlabel].add(smt[3])
                    if smt[4] not in alldefd[nowlabel]:
                        used[nowlabel].add(smt[4])
                    allused[nowlabel].add(smt[4])
                    if smt[2] not in allused[nowlabel]:
                        defd[nowlabel].add(smt[2])
                    alldefd[nowlabel].add(smt[2])
                elif smt[0] == lrEnum.li:
                    if smt[1] not in allused[nowlabel]:
                        defd[nowlabel].add(smt[1])
                    alldefd[nowlabel].add(smt[1])
                elif smt[0] == lrEnum.ret:
                    continue
                elif smt[0] == lrEnum.call:
                    self.needra = True
                    for reg in caller:
                        if reg not in allused[nowlabel]:
                            defd[nowlabel].add(reg)
                        alldefd[nowlabel].add(reg)
                elif smt[0] == lrEnum.sw:
                    if smt[1] not in alldefd[nowlabel]:
                        used[nowlabel].add(smt[1])
                    allused[nowlabel].add(smt[1])
                    if smt[3] not in alldefd[nowlabel]:
                        used[nowlabel].add(smt[3])
                    allused[nowlabel].add(smt[3])
                elif smt[0] == lrEnum.lui:
                    if smt[1] not in allused[nowlabel]:
                        defd[nowlabel].add(smt[1])
                    alldefd[nowlabel].add(smt[1])
                elif smt[0] == lrEnum.icmp:
                    if smt[2] not in allused[nowlabel]:
                        defd[nowlabel].add(smt[2])
                    alldefd[nowlabel].add(smt[2])
                    if smt[3] not in alldefd[nowlabel]:
                        used[nowlabel].add(smt[3])
                    allused[nowlabel].add(smt[3])
                elif smt[0] == lrEnum.j:
                    if nowlabel not in next:
                        next[nowlabel] = set()
                    next[nowlabel].add(smt[2])
                    if smt[2] not in pre:
                        pre[smt[2]] = set()
                    pre[smt[2]].add(nowlabel)
                elif smt[0] == lrEnum.bnez:
                    if nowlabel not in next:
                        next[nowlabel] = set()
                    next[nowlabel].add(smt[3])
                    if smt[3] not in pre:
                        pre[smt[3]] = set()
                    pre[smt[3]].add(nowlabel)
                    if smt[1] not in alldefd[nowlabel]:
                        used[nowlabel].add(smt[1])
                    allused[nowlabel].add(smt[1])
                elif smt[0] == lrEnum.binaryi:
                    if smt[3] not in alldefd[nowlabel]:
                        used[nowlabel].add(smt[3])
                    allused[nowlabel].add(smt[3])
                    if smt[2] not in allused[nowlabel]:
                        defd[nowlabel].add(smt[2])
                    alldefd[nowlabel].add(smt[2])
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
            for i in range(len(alllabel[label]) - 1, -1, -1):
                smt = alllabel[label][i]
                if begin:
                    begin = False
                    liveout[label][i] = allout[label]
                    continue
                smt = alllabel[label][i + 1]
                liveout[label][i] = liveout[label][i + 1].copy()
                if smt[0] == lrEnum.mv:
                    liveout[label][i].discard(smt[1])
                    liveout[label][i].add(smt[2])
                elif smt[0] == lrEnum.lw:
                    liveout[label][i].discard(smt[1])
                    liveout[label][i].add(smt[3])
                elif smt[0] == lrEnum.binary:
                    liveout[label][i].discard(smt[2])
                    liveout[label][i].add(smt[3])
                    liveout[label][i].add(smt[4])
                elif smt[0] == lrEnum.li:
                    liveout[label][i].discard(smt[1])
                elif smt[0] == lrEnum.call:
                    for reg in caller:
                        liveout[label][i].discard(reg)
                elif smt[0] == lrEnum.sw:
                    liveout[label][i].add(smt[1])
                    liveout[label][i].add(smt[3])
                elif smt[0] == lrEnum.lui:
                    liveout[label][i].discard(smt[1])
                elif smt[0] == lrEnum.icmp:
                    liveout[label][i].discard(smt[2])
                    liveout[label][i].add(smt[3])
                elif smt[0] == lrEnum.bnez:
                    liveout[label][i].add(smt[1])
                elif smt[0] == lrEnum.binaryi:
                    liveout[label][i].discard(smt[2])
                    liveout[label][i].add(smt[3])
        edges = {}
        for label in alllabel:
            for i in range(len(alllabel[label])):
                smt = alllabel[label][i]
                if smt[0] == lrEnum.mv:
                    if smt[1] not in edges:
                        edges[smt[1]] = set()
                    for cri in liveout[label][i]:
                        if cri not in edges:
                            edges[cri] = set()
                        edges[cri].add(smt[1])
                        edges[smt[1]].add(cri)
                elif smt[0] == lrEnum.lw:
                    if smt[1] not in edges:
                        edges[smt[1]] = set()
                    for cri in liveout[label][i]:
                        if cri not in edges:
                            edges[cri] = set()
                        edges[cri].add(smt[1])
                        edges[smt[1]].add(cri)
                elif smt[0] == lrEnum.binary:
                    if smt[2] not in edges:
                        edges[smt[2]] = set()
                    for cri in liveout[label][i]:
                        if cri not in edges:
                            edges[cri] = set()
                        edges[cri].add(smt[2])
                        edges[smt[2]].add(cri)
                elif smt[0] == lrEnum.li:
                    if smt[1] not in edges:
                        edges[smt[1]] = set()
                    for cri in liveout[label][i]:
                        if cri not in edges:
                            edges[cri] = set()
                        edges[cri].add(smt[1])
                        edges[smt[1]].add(cri)
                elif smt[0] == lrEnum.call:
                    for reg in caller:
                        if reg not in edges:
                            edges[reg] = set()
                        for cri in liveout[label][i]:
                            if cri not in edges:
                                edges[cri] = set()
                            edges[cri].add(reg)
                            edges[reg].add(cri)
                elif smt[0] == lrEnum.lui:
                    if smt[1] not in edges:
                        edges[smt[1]] = set()
                    for cri in liveout[label][i]:
                        if cri not in edges:
                            edges[cri] = set()
                        edges[cri].add(smt[1])
                        edges[smt[1]].add(cri)
                elif smt[0] == lrEnum.icmp:
                    if smt[2] not in edges:
                        edges[smt[2]] = set()
                    for cri in liveout[label][i]:
                        if cri not in edges:
                            edges[cri] = set()
                        edges[cri].add(smt[2])
                        edges[smt[2]].add(cri)
                elif smt[0] == lrEnum.binaryi:
                    if smt[2] not in edges:
                        edges[smt[2]] = set()
                    for cri in liveout[label][i]:
                        if cri not in edges:
                            edges[cri] = set()
                        edges[cri].add(smt[2])
                        edges[smt[2]].add(cri)
        for reg in edges:
            edges[reg].discard(reg)
            edges[reg].discard('sp')
        if 'sp' in edges:
            edges.pop('sp')
        return mvlib, mvlist, edges

    def make(self, funcname, array, dt):
        self.varnum = 0
        tempblock = 0
        varbank = {}
        tempconst = {}
        ret = []
        allblock = {'entry': [[lrEnum.label, funcname, 'entry']]}
        alllabel = {}
        for i in range(len(array[1])):
            if i < 8:
                varname = self.getreg(varbank, array[1][i][1])
                allblock['entry'].append([lrEnum.mv, varname, f'a{i}'])
            else:
                varname = self.getreg(varbank, array[1][i][1])
                allblock['entry'].append([lrEnum.lw, varname, (i - 8) * 4, 'sp'])
        pre = {}
        next = {}
        phi = {}
        for label in array[2]:
            nowlabel = ""
            for smt in label:
                if smt[0] == llvmEnum.Label:
                    nowlabel = smt[1]
                    alllabel[nowlabel] = label
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
        queue = ['entry']
        while len(queue) > 0:
            name = queue.pop(0)
            if name not in alllabel:
                continue
            label = alllabel[name]
            nowlabel = ""
            for smt in label:
                if smt[0] == llvmEnum.Pass:
                    continue
                elif smt[0] == llvmEnum.Label:
                    nowlabel = smt[1]
                    if nowlabel not in allblock:
                        allblock[nowlabel] = [[lrEnum.label, funcname, nowlabel]]
                    ret.append(allblock[nowlabel])
                elif smt[0] == llvmEnum.Alloca:
                    raise Exception("No Alloca!")
                elif smt[0] == llvmEnum.Binary:
                    lhsvalue, lhscheck = self.constcheck(tempconst, smt[4])
                    rhsvalue, rhscheck = self.constcheck(tempconst, smt[5])
                    if lhscheck and rhscheck:
                        tempconst[smt[1]] = self.getvalue(smt[2], lhsvalue, rhsvalue)
                    else:
                        varname = self.getreg(varbank, smt[1])
                        if lhscheck:
                            allblock[nowlabel].append([lrEnum.li, varname, lhsvalue])
                            allblock[nowlabel].append([lrEnum.binary, binaryopt[smt[2]], varname, varname, self.getreg(varbank, smt[5])])
                        elif rhscheck:
                            if smt[2] in ['mul', 'sdiv', 'srem']:
                                tempname = f"temp_{self.varnum}"
                                self.varnum += 1
                                allblock[nowlabel].append([lrEnum.li, tempname, smt[5]])
                                allblock[nowlabel].append([lrEnum.binary, binaryopt[smt[2]], varname, self.getreg(varbank, smt[4]), tempname])
                            else:
                                allblock[nowlabel].append([lrEnum.binaryi, binaryopt[smt[2]] + 'i', varname, self.getreg(varbank, smt[4]), rhsvalue])
                        else:
                            allblock[nowlabel].append([lrEnum.binary, binaryopt[smt[2]], varname, self.getreg(varbank, smt[4]), self.getreg(varbank, smt[5])])
                elif smt[0] == llvmEnum.Return:
                    retvalue, retcheck = self.constcheck(tempconst, smt[2])
                    if retcheck:
                        allblock[nowlabel].append([lrEnum.li, 'a0', retvalue])
                    else:
                        if smt[2] in varbank:
                            allblock[nowlabel].append([lrEnum.mv, 'a0', varbank[smt[2]]])
                        else:
                            if smt[2][0] != '@':
                                varname = f"temp_{self.varnum}"
                                self.varnum += 1
                                varbank[smt[2]] = varname
                                allblock[nowlabel].append([lrEnum.mv, 'a0', varname])
                            else:
                                allblock[nowlabel].append([lrEnum.lui, 'a0', arg[1][1:]])
                                allblock[nowlabel].append([lrEnum.binaryi, 'addi', 'a0', 'a0', f'%lo({arg[1][1:]})'])
                    allblock[nowlabel].append([lrEnum.ret])
                elif smt[0] == llvmEnum.ReturnVoid:
                    allblock[nowlabel].append([lrEnum.ret])
                elif smt[0] == llvmEnum.FuncCall:
                    self.funcarg = max(self.funcarg, len(smt[4]) - 8)
                    for i in range(len(smt[4])):
                        arg = smt[4][i]
                        argvalue, argcheck = self.constcheck(tempconst, arg[1])
                        if i < 8:
                            if argcheck:
                                allblock[nowlabel].append([lrEnum.li, f'a{i}', argvalue])
                            else:
                                if arg[1] in varbank:
                                    allblock[nowlabel].append([lrEnum.mv, f'a{i}', varbank[arg[1]]])
                                else:
                                    if arg[1][0] != '@':
                                        varname = f"temp_{self.varnum}"
                                        self.varnum += 1
                                        varbank[arg[1]] = varname
                                        allblock[nowlabel].append([lrEnum.mv, f'a{i}', varname])
                                    else:
                                        allblock[nowlabel].append([lrEnum.lui, f'a{i}', arg[1][1:]])
                                        allblock[nowlabel].append([lrEnum.binaryi, 'addi', f'a{i}', f'a{i}', f'%lo({arg[1][1:]})'])
                        else:
                            if argcheck:
                                varname = f"temp_{self.varnum}"
                                self.varnum += 1
                                allblock[nowlabel].append([lrEnum.li, varname, argvalue])
                                allblock[nowlabel].append([lrEnum.sw, varname, (i - 8) * 4, 'arg'])
                            else:
                                if arg[1] in varbank:
                                    allblock[nowlabel].append([lrEnum.sw, varbank[arg[1]], (i - 8) * 4, 'arg'])
                                else:
                                    if arg[1][0] != '@':
                                        varname = f"temp_{self.varnum}"
                                        self.varnum += 1
                                        varbank[arg[1]] = varname
                                        allblock[nowlabel].append([lrEnum.sw, varname, (i - 8) * 4, 'arg'])
                                    else:
                                        varname = f"temp_{self.varnum}"
                                        self.varnum += 1
                                        allblock[nowlabel].append([lrEnum.lui, varname, arg[1][1:]])
                                        allblock[nowlabel].append([lrEnum.binaryi, 'addi', varname, varname, f'%lo({arg[1][1:]})'])
                                        allblock[nowlabel].append([lrEnum.sw, varname, (i - 8) * 4, 'arg'])
                    varname = self.getreg(varbank, smt[1])
                    allblock[nowlabel].append([lrEnum.call, smt[3]])
                    allblock[nowlabel].append([lrEnum.mv, varname, 'a0'])
                elif smt[0] == llvmEnum.FuncVoid:
                    self.funcarg = max(self.funcarg, len(smt[2]) - 8)
                    for i in range(len(smt[2])):
                        arg = smt[2][i]
                        argvalue, argcheck = self.constcheck(tempconst, arg[1])
                        if i < 8:
                            if argcheck:
                                allblock[nowlabel].append([lrEnum.li, f'a{i}', argvalue])
                            else:
                                if arg[1] in varbank:
                                    allblock[nowlabel].append([lrEnum.mv, f'a{i}', varbank[arg[1]]])
                                else:
                                    if arg[1][0] != '@':
                                        varname = f"temp_{self.varnum}"
                                        self.varnum += 1
                                        varbank[arg[1]] = varname
                                        allblock[nowlabel].append([lrEnum.mv, f'a{i}', varname])
                                    else:
                                        allblock[nowlabel].append([lrEnum.lui, f'a{i}', arg[1][1:]])
                                        allblock[nowlabel].append([lrEnum.binaryi, 'addi', f'a{i}', f'a{i}', f'%lo({arg[1][1:]})'])
                        else:
                            if argcheck:
                                varname = f"temp_{self.varnum}"
                                self.varnum += 1
                                allblock[nowlabel].append([lrEnum.li, varname, argvalue])
                                allblock[nowlabel].append([lrEnum.sw, varname, (i - 8) * 4, 'arg'])
                            else:
                                if arg[1] in varbank:
                                    allblock[nowlabel].append([lrEnum.sw, varbank[arg[1]], (i - 8) * 4, 'arg'])
                                else:
                                    if arg[1][0] != '@':
                                        varname = f"temp_{self.varnum}"
                                        self.varnum += 1
                                        varbank[arg[1]] = varname
                                        allblock[nowlabel].append([lrEnum.sw, varname, (i - 8) * 4, 'arg'])
                                    else:
                                        varname = f"temp_{self.varnum}"
                                        self.varnum += 1
                                        allblock[nowlabel].append([lrEnum.lui, varname, arg[1][1:]])
                                        allblock[nowlabel].append([lrEnum.binaryi, 'addi', varname, varname, f'%lo({arg[1][1:]})'])
                                        allblock[nowlabel].append([lrEnum.sw, varname, (i - 8) * 4, 'arg'])
                    allblock[nowlabel].append([lrEnum.call, smt[1]])
                elif smt[0] == llvmEnum.Trunc:
                    if smt[1] in varbank:
                        if smt[2] in tempconst:
                            allblock[nowlabel].append([lrEnum.li, varbank[smt[1]], tempconst[smt[2]]])
                        else:
                            allblock[nowlabel].append([lrEnum.mv, varbank[smt[1]], self.getreg(varbank, smt[2])])
                    else:
                        if smt[2] in tempconst:
                            tempconst[smt[1]] = tempconst[smt[2]]
                        else:
                            varbank[smt[1]] = self.getreg(varbank, smt[2])
                elif smt[0] == llvmEnum.Zext:
                    if smt[1] in varbank:
                        if smt[2] in tempconst:
                            allblock[nowlabel].append([lrEnum.li, varbank[smt[1]], tempconst[smt[2]]])
                        else:
                            allblock[nowlabel].append([lrEnum.mv, varbank[smt[1]], self.getreg(varbank, smt[2])])
                    else:
                        if smt[2] in tempconst:
                            tempconst[smt[1]] = tempconst[smt[2]]
                        else:
                            varbank[smt[1]] = self.getreg(varbank, smt[2])
                elif smt[0] == llvmEnum.Phi:
                    if smt[1] not in varbank:
                        varname = f"temp_{self.varnum}"
                        self.varnum += 1
                        varbank[smt[1]] = varname
                elif smt[0] == llvmEnum.Icmp:
                    lhsvalue, lhscheck = self.constcheck(tempconst, smt[4])
                    rhsvalue, rhscheck = self.constcheck(tempconst, smt[5])
                    if lhscheck and rhscheck:
                        if smt[2] == 'eq':
                            tempconst[smt[1]] = int(lhsvalue == rhsvalue)
                        elif smt[2] == 'ne':
                            tempconst[smt[1]] = int(lhsvalue != rhsvalue)
                        elif smt[2] == 'slt':
                            tempconst[smt[1]] = int(lhsvalue < rhsvalue)
                        elif smt[2] == 'sgt':
                            tempconst[smt[1]] = int(lhsvalue > rhsvalue)
                        elif smt[2] == 'sle':
                            tempconst[smt[1]] = int(lhsvalue <= rhsvalue)
                        elif smt[2] == 'sge':
                            tempconst[smt[1]] = int(lhsvalue >= rhsvalue)
                        else:
                            raise Exception("Warning in icmp")
                    else:
                        varname = self.getreg(varbank, smt[1])
                        if lhscheck:
                            allblock[nowlabel].append([lrEnum.li, varname, lhsvalue])
                            rhsvalue = self.getreg(varbank, smt[5])
                            lhsvalue = varname
                        elif rhscheck:
                            allblock[nowlabel].append([lrEnum.li, varname, rhsvalue])
                            lhsvalue = self.getreg(varbank, smt[4])
                            rhsvalue = varname
                        else:
                            lhsvalue = self.getreg(varbank, smt[4])
                            rhsvalue = self.getreg(varbank, smt[5])
                        if smt[2] == 'eq':
                            allblock[nowlabel].append([lrEnum.binary, 'xor', varname, lhsvalue, rhsvalue])
                            allblock[nowlabel].append([lrEnum.icmp, 'seqz', varname, varname])
                        elif smt[2] == 'ne':
                            allblock[nowlabel].append([lrEnum.binary, 'xor', varname, lhsvalue, rhsvalue])
                            allblock[nowlabel].append([lrEnum.icmp, 'snez', varname, varname])
                        elif smt[2] == 'slt':
                            allblock[nowlabel].append([lrEnum.binary, 'slt', varname, lhsvalue, rhsvalue])
                        elif smt[2] == 'sgt':
                            allblock[nowlabel].append([lrEnum.binary, 'slt', varname, rhsvalue, lhsvalue])
                        elif smt[2] == 'sle':
                            allblock[nowlabel].append([lrEnum.binary, 'slt', varname, rhsvalue, lhsvalue])
                            allblock[nowlabel].append([lrEnum.binaryi, 'xori', varname, varname, 1])
                        elif smt[2] == 'sge':
                            allblock[nowlabel].append([lrEnum.binary, 'slt', varname, lhsvalue, rhsvalue])
                            allblock[nowlabel].append([lrEnum.binaryi, 'xori', varname, varname, 1])
                        else:
                            raise Exception("Warning in icmp")
                elif smt[0] == llvmEnum.Getelementptr1:
                    tarReg = self.getreg(varbank, smt[3])
                    indvalue, indcheck = self.constcheck(tempconst, smt[4])
                    varname = self.getreg(varbank, smt[1])
                    if indcheck:
                        if indvalue != 0:
                            allblock[nowlabel].append([lrEnum.binaryi, 'addi', varname, tarReg, indvalue * 4])
                        else:
                            allblock[nowlabel].append([lrEnum.mv, varname, tarReg])
                    else:
                        allblock[nowlabel].append([lrEnum.binaryi, 'slli', varname, self.getreg(varbank, smt[4]), 2])
                        allblock[nowlabel].append([lrEnum.binary, 'add', varname, tarReg, varname])
                elif smt[0] == llvmEnum.Getelementptr2:
                    tarReg = self.getreg(varbank, smt[3])
                    indvalue, indcheck = self.constcheck(tempconst, smt[4])
                    varname = self.getreg(varbank, smt[1])
                    if indcheck:
                        if indvalue != 0:
                            allblock[nowlabel].append([lrEnum.binaryi, 'addi', varname, tarReg, indvalue * 4])
                        else:
                            allblock[nowlabel].append([lrEnum.mv, varname, tarReg])
                    else:
                        allblock[nowlabel].append([lrEnum.binaryi, 'slli', varname, self.getreg(varbank, smt[4]), 2])
                        allblock[nowlabel].append([lrEnum.binary, 'add', varname, tarReg, varname])
                elif smt[0] == llvmEnum.Load:
                    if smt[3] == '@.true':
                        tempconst[smt[1]] = 1
                    elif smt[3] == '@.false':
                        tempconst[smt[1]] = 0
                    else:
                        varname = self.getreg(varbank, smt[1])
                        if smt[3] in varbank:
                            allblock[nowlabel].append([lrEnum.lw, varname, 0, varbank[smt[3]]])
                        else:
                            if smt[3][0] != '@':
                                raise Exception("Warning in Load at @")
                            allblock[nowlabel].append([lrEnum.lui, varname, smt[3][1:]])
                            allblock[nowlabel].append([lrEnum.lw, varname, f"%lo({smt[3][1:]})", varname])
                elif smt[0] == llvmEnum.Store:
                    varvalue, varcheck = self.constcheck(tempconst, smt[2])
                    if varcheck:
                        varname = f"temp_{self.varnum}"
                        self.varnum += 1
                        allblock[nowlabel].append([lrEnum.li, varname, varvalue])
                    else:
                        if smt[2] not in varbank:
                            if smt[2][0] != '@':
                                varname = self.getreg(varbank, smt[2])
                            else:
                                varname = f"temp_{self.varnum}"
                                self.varnum += 1
                                allblock[nowlabel].append([lrEnum.lui, varname, smt[2][1:]])
                                allblock[nowlabel].append([lrEnum.binaryi, 'addi', varname, varname, f'%lo({smt[2][1:]})'])
                        else:
                            varname = self.getreg(varbank, smt[2])
                    if smt[3] not in varbank:
                        if smt[3][0] != "@":
                            tarReg = f"temp_{self.varnum}"
                            self.varnum += 1
                            varbank[smt[3]] = tarReg
                            allblock[nowlabel].append([lrEnum.sw, varname, 0, tarReg])
                        else:
                            tarReg = f"temp_{self.varnum}"
                            self.varnum += 1
                            allblock[nowlabel].append([lrEnum.lui, tarReg, smt[3][1:]])
                            allblock[nowlabel].append([lrEnum.sw, varname, f"%lo({smt[3][1:]})", tarReg])
                    else:
                        allblock[nowlabel].append([lrEnum.sw, varname, 0, varbank[smt[3]]])
                elif smt[0] == llvmEnum.Jump:
                    if (nowlabel in phi) and (smt[1] in phi[nowlabel]):
                        phibank = {}
                        for arg in phi[nowlabel][smt[1]]:
                            if arg[1] not in phibank:
                                varvalue, varcheck = self.constcheck(tempconst, arg[1])
                                if varcheck:
                                    tarReg = self.getreg(varbank, arg[0])
                                    allblock[nowlabel].append([lrEnum.li, tarReg, varvalue])
                                else:
                                    if arg[1] in varbank:
                                        varname = varbank[arg[1]]
                                        tempname = f"temp_{self.varnum}"
                                        self.varnum += 1
                                        phibank[arg[1]] = tempname
                                        allblock[nowlabel].append([lrEnum.mv, tempname, varname])
                                    else:
                                        if arg[1][0] != '@':
                                            tempvar = self.getreg(varbank, arg[1])
                                            varname = f"temp_{self.varnum}"
                                            self.varnum += 1
                                            phibank[arg[1]] = varname
                                            allblock[nowlabel].append([lrEnum.mv, varname, tempvar])
                                        else:
                                            tarReg = self.getreg(varbank, arg[0])
                                            allblock[nowlabel].append([lrEnum.lui, tarReg, arg[1][1:]])
                                            allblock[nowlabel].append([lrEnum.binaryi, 'addi', tarReg, tarReg, f'%lo({arg[1][1:]})'])
                        for arg in phi[nowlabel][smt[1]]:
                            if arg[1] in phibank:
                                tarReg = self.getreg(varbank, arg[0])
                                allblock[nowlabel].append([lrEnum.mv, tarReg, phibank[arg[1]]])
                    allblock[nowlabel].append([lrEnum.j, funcname, smt[1]])
                elif smt[0] == llvmEnum.Br:
                    brvalue, brcheck = self.constcheck(tempconst, smt[1])
                    if brcheck:
                        if brvalue == 1:
                            if nowlabel in phi and smt[2] in phi[nowlabel]:
                                phibank = {}
                                for arg in phi[nowlabel][smt[2]]:
                                    if arg[1] not in phibank:
                                        varvalue, varcheck = self.constcheck(tempconst, arg[1])
                                        if varcheck:
                                            tarReg = self.getreg(varbank, arg[0])
                                            allblock[nowlabel].append([lrEnum.li, tarReg, varvalue])
                                        else:
                                            if arg[1] in varbank:
                                                varname = varbank[arg[1]]
                                                tempname = f"temp_{self.varnum}"
                                                self.varnum += 1
                                                phibank[arg[1]] = tempname
                                                allblock[nowlabel].append([lrEnum.mv, tempname, varname])
                                            else:
                                                if arg[1][0] != '@':
                                                    tempvar = self.getreg(varbank, arg[1])
                                                    varname = f"temp_{self.varnum}"
                                                    self.varnum += 1
                                                    phibank[arg[1]] = varname
                                                    allblock[nowlabel].append([lrEnum.mv, varname, tempvar])
                                                else:
                                                    tarReg = self.getreg(varbank, arg[0])
                                                    allblock[nowlabel].append([lrEnum.lui, tarReg, arg[1][1:]])
                                                    allblock[nowlabel].append([lrEnum.binaryi, 'addi', tarReg, tarReg, f'%lo({arg[1][1:]})'])
                                for arg in phi[nowlabel][smt[2]]:
                                    if arg[1] in phibank:
                                        tarReg = self.getreg(varbank, arg[0])
                                        allblock[nowlabel].append([lrEnum.mv, tarReg, phibank[arg[1]]])
                            allblock[nowlabel].append([lrEnum.j, funcname, smt[2]])
                        elif brvalue == 0:
                            if nowlabel in phi and smt[3] in phi[nowlabel]:
                                phibank = {}
                                for arg in phi[nowlabel][smt[3]]:
                                    if arg[1] not in phibank:
                                        varvalue, varcheck = self.constcheck(tempconst, arg[1])
                                        if varcheck:
                                            tarReg = self.getreg(varbank, arg[0])
                                            allblock[nowlabel].append([lrEnum.li, tarReg, varvalue])
                                        else:
                                            if arg[1] in varbank:
                                                varname = varbank[arg[1]]
                                                phibank[arg[1]] = varname
                                            else:
                                                if arg[1][0] != '@':
                                                    tempvar = self.getreg(varbank, arg[1])
                                                    varname = f"temp_{self.varnum}"
                                                    self.varnum += 1
                                                    phibank[arg[1]] = varname
                                                    allblock[nowlabel].append([lrEnum.mv, varname, tempvar])
                                                else:
                                                    tarReg = self.getreg(varbank, arg[0])
                                                    allblock[nowlabel].append([lrEnum.lui, tarReg, arg[1][1:]])
                                                    allblock[nowlabel].append([lrEnum.binaryi, 'addi', tarReg, tarReg, f'%lo({arg[1][1:]})'])
                                for arg in phi[nowlabel][smt[3]]:
                                    if arg[1] in phibank:
                                        tarReg = self.getreg(varbank, arg[0])
                                        allblock[nowlabel].append([lrEnum.mv, tarReg, phibank[arg[1]]])
                            allblock[nowlabel].append([lrEnum.j, funcname, smt[3]])
                        else:
                            raise Exception("Warning in Br")
                    else:
                        brReg = self.getreg(varbank, smt[1])
                        if nowlabel in phi and smt[2] in phi[nowlabel]:
                            lhslabel = f"phiblock_{tempblock}"
                            tempblock += 1
                            newblock1 = [[lrEnum.label, funcname, lhslabel]]
                            phibank = {}
                            for arg in phi[nowlabel][smt[2]]:
                                if arg[1] not in phibank:
                                    varvalue, varcheck = self.constcheck(tempconst, arg[1])
                                    if varcheck:
                                        tarReg = self.getreg(varbank, arg[0])
                                        newblock1.append([lrEnum.li, tarReg, varvalue])
                                    else:
                                        if arg[1] in varbank:
                                            varname = varbank[arg[1]]
                                            phibank[arg[1]] = varname
                                        else:
                                            if arg[1][0] != '@':
                                                tempvar = self.getreg(varbank, arg[1])
                                                varname = f"temp_{self.varnum}"
                                                self.varnum += 1
                                                phibank[arg[1]] = varname
                                                newblock1.append([lrEnum.mv, varname, tempvar])
                                            else:
                                                tarReg = self.getreg(varbank, arg[0])
                                                newblock1.append([lrEnum.lui, tarReg, arg[1][1:]])
                                                newblock1.append([lrEnum.binaryi, 'addi', tarReg, tarReg, f'%lo({arg[1][1:]})'])
                            for arg in phi[nowlabel][smt[2]]:
                                if arg[1] in phibank:
                                    tarReg = self.getreg(varbank, arg[0])
                                    newblock1.append([lrEnum.mv, tarReg, phibank[arg[1]]])
                            newblock1.append([lrEnum.j, funcname, smt[2]])
                            ret.append(newblock1)
                        else:
                            lhslabel = smt[2]
                        allblock[nowlabel].append([lrEnum.bnez, brReg, funcname, lhslabel])
                        if nowlabel in phi and smt[3] in phi[nowlabel]:
                            rhslabel = f"phiblock_{tempblock}"
                            tempblock += 1
                            newblock2 = [[lrEnum.label, funcname, rhslabel]]
                            phibank = {}
                            for arg in phi[nowlabel][smt[3]]:
                                if arg[1] not in phibank:
                                    varvalue, varcheck = self.constcheck(tempconst, arg[1])
                                    if varcheck:
                                        tarReg = self.getreg(varbank, arg[0])
                                        newblock2.append([lrEnum.li, tarReg, varvalue])
                                    else:
                                        if arg[1] in varbank:
                                            varname = varbank[arg[1]]
                                            phibank[arg[1]] = varname
                                        else:
                                            if arg[1][0] != '@':
                                                tempvar = self.getreg(varbank, arg[1])
                                                varname = f"temp_{self.varnum}"
                                                self.varnum += 1
                                                phibank[arg[1]] = varname
                                                newblock2.append([lrEnum.mv, varname, tempvar])
                                            else:
                                                tarReg = self.getreg(varbank, arg[0])
                                                newblock2.append([lrEnum.lui, tarReg, arg[1][1:]])
                                                newblock2.append([lrEnum.binaryi, 'addi', tarReg, tarReg, f'%lo({arg[1][1:]})'])
                            for arg in phi[nowlabel][smt[3]]:
                                if arg[1] in phibank:
                                    tarReg = self.getreg(varbank, arg[0])
                                    newblock2.append([lrEnum.mv, tarReg, phibank[arg[1]]])
                            newblock2.append([lrEnum.j, funcname, smt[3]])
                            ret.append(newblock2)
                        else:
                            rhslabel = smt[3]
                        allblock[nowlabel].append([lrEnum.j, funcname, rhslabel])
                else:
                    raise Exception("Warning")
            for suc in dt[nowlabel]:
                queue.append(suc)
        return ret

    def constcheck(self, tempconst, var):
        if var == 'true':
            return 1, True
        if var == 'false':
            return 0, True
        if var == 'null':
            return 0, True
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
            if rhs == 0:
                return 0;
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

    def getreg(self, varbank, var):
        if var in varbank:
            return varbank[var]
        varname = f"temp_{self.varnum}"
        self.varnum += 1
        varbank[var] = varname
        return varname

    def makeworklist(self, mvlib, graph, movelist, activemMove):
        spillworklist = []
        freezeworklist = []
        simplifyworklist = []
        for i in range(self.varnum):
            varname = f"temp_{i}"
            if varname in graph:
                degree = len(graph[varname])
            else:
                degree = 0
            if degree >= len(reg2use):
                spillworklist.append(varname)
            elif self.mvrelated(varname, movelist, activemMove, mvlib):
                freezeworklist.append(varname)
            else:
                simplifyworklist.append(varname)
        return spillworklist, freezeworklist, simplifyworklist

    def simplify(self, simplifyworklist, selectStack, mvlib, movelist, graph, activemMove, coalescedNodes, spillworklist, freezeworklist):
        tosimplify = simplifyworklist.pop(0)
        if tosimplify in reg2use:
            return
        selectStack.append(tosimplify)
        if tosimplify in graph:
            for suc in graph[tosimplify]:
                if suc not in selectStack and suc not in coalescedNodes:
                    graph[suc].discard(tosimplify)
                    degree = len(graph[suc])
                    if degree == len(reg2use) - 1:
                        for sucsuc in graph[suc]:
                            if sucsuc not in selectStack and sucsuc not in coalescedNodes and sucsuc in movelist:
                                for m in movelist[sucsuc]:
                                    if m in activemMove:
                                        activemMove.remove(m)
                                        mvlib.append(m)
                        if suc in spillworklist:
                            spillworklist.remove(suc)
                        if self.mvrelated(suc, movelist, activemMove, mvlib):
                            if suc not in freezeworklist:
                                freezeworklist.append(suc)
                        else:
                            if suc not in simplifyworklist:
                                simplifyworklist.append(suc)

    def coalesce(self, spillworklist, selectStack, mvlib, movelist, graph, activemMove, constrainedMove, coalescedMove, coalescedNodes,
                 freezeworklist, simplifyworklist):
        tocoalesce = mvlib.pop(0)
        x = self.alias(coalescedNodes, tocoalesce[0])
        y = self.alias(coalescedNodes, tocoalesce[1])
        if y in reg2use:
            u, v = y, x
        else:
            u, v = x, y
        if u == v:
            coalescedMove.append(tocoalesce)
            self.addWork(u, graph, freezeworklist, simplifyworklist, movelist, activemMove, mvlib)
        elif v in reg2use or (u in graph and v in graph[u]):
            constrainedMove.append(tocoalesce)
            self.addWork(u, graph, freezeworklist, simplifyworklist, movelist, activemMove, mvlib)
            self.addWork(v, graph, freezeworklist, simplifyworklist, movelist, activemMove, mvlib)
        elif u in reg2use:
            if v not in graph:
                graph[v] = set()
            flag = True
            for t in graph[v]:
                if t not in selectStack and t not in coalescedNodes:
                    if t in graph:
                        degree = len(graph[t])
                    else:
                        degree = 0
                    flag = flag and (degree < len(reg2use) or t in reg2use or (u in graph and t in graph[u]))
            if flag:
                coalescedMove.append(tocoalesce)
                self.Combine(graph, u, v, freezeworklist, spillworklist, coalescedNodes, activemMove, mvlib, movelist, selectStack, simplifyworklist)
                self.addWork(u, graph, freezeworklist, simplifyworklist, movelist, activemMove, mvlib)
            else:
                activemMove.append(tocoalesce)
        else:
            newnode = set()
            num = 0
            if u in graph:
                for suc in graph[u]:
                    if suc not in selectStack and suc not in coalescedNodes:
                        newnode.add(suc)
            if v in graph:
                for suc in graph[v]:
                    if suc not in selectStack and suc not in coalescedNodes:
                        newnode.add(suc)
            for node in newnode:
                if node not in graph:
                    degree = 0
                else:
                    degree = len(graph[node])
                if degree >= len(reg2use):
                    num += 1
            if num < len(reg2use):
                coalescedMove.append(tocoalesce)
                self.Combine(graph, u, v, freezeworklist, spillworklist, coalescedNodes, activemMove, mvlib, movelist, selectStack, simplifyworklist)
                self.addWork(u, graph, freezeworklist, simplifyworklist, movelist, activemMove, mvlib)
            else:
                activemMove.append(tocoalesce)

    def alias(self, coalescedNodes, name):
        if name in coalescedNodes:
            return self.alias(coalescedNodes, coalescedNodes[name])
        else:
            return name

    def addWork(self, name, graph, freezeworklist, simplifyworklist, movelist, activemMove, mvlib):
        if name not in reg2use and not (self.mvrelated(name, movelist, activemMove, mvlib)):
            if name in graph:
                degree = len(graph[name])
            else:
                degree = 0
            if degree < len(reg2use):
                if name not in simplifyworklist:
                    simplifyworklist.append(name)
                if name in freezeworklist:
                    freezeworklist.remove(name)

    def Combine(self, graph, u, v, freezeworklist, spillworklist, coalescedNodes, activemMove, mvlib, movelist, selectStack, simplifyworklist):
        if v in freezeworklist:
            freezeworklist.remove(v)
        if v in spillworklist:
            spillworklist.remove(v)
        coalescedNodes[v] = u
        for mv in movelist[v]:
            movelist[u].append(mv)
        for m in movelist[v]:
            if m in activemMove:
                activemMove.remove(m)
                mvlib.append(m)
        if u not in graph:
            graph[u] = set()
        if v not in graph:
            graph[v] = set()
        for t in graph[v]:
            graph[t].add(u)
            graph[t].discard(v)
            graph[u].add(t)
            degree = len(graph[t])
            if degree == len(reg2use) - 1:
                for sucsuc in graph[t]:
                    if sucsuc not in selectStack and sucsuc not in coalescedNodes and sucsuc in movelist:
                        for m in movelist[sucsuc]:
                            if m in activemMove:
                                activemMove.remove(m)
                                mvlib.append(m)
                if t in spillworklist:
                    spillworklist.remove(t)
                if self.mvrelated(t, movelist, activemMove, mvlib):
                    if t not in freezeworklist:
                        freezeworklist.append(t)
                else:
                    if t not in simplifyworklist:
                        simplifyworklist.append(t)

        degree = len(graph[u])
        if degree >= len(reg2use):
            if u in freezeworklist:
                freezeworklist.remove(u)
            if u not in spillworklist:
                spillworklist.append(u)

    def freeze(self, freezeworklist, simplifyworklist, movelist, mvlib, activemMove, coalescedNodes, frozenlist, graph):
        u = freezeworklist.pop(0)
        if u not in simplifyworklist:
            simplifyworklist.append(u)
        for m in movelist[u]:
            if m in activemMove or m in mvlib:
                x, y = m[0], m[1]
                if self.alias(coalescedNodes, y) == self.alias(coalescedNodes, u):
                    v = self.alias(coalescedNodes, x)
                else:
                    v = self.alias(coalescedNodes, y)
                activemMove.remove(m)
                frozenlist.append(m)
                if v in graph:
                    degree = len(graph[v])
                else:
                    degree = 0
                if self.mvrelated(v, movelist, activemMove, mvlib) and degree < len(reg2use):
                    freezeworklist.remove(v)
                    if v not in simplifyworklist:
                        simplifyworklist.append(v)

    def selectspill(self, spillworklist, simplifyworklist, movelist, activemMove, mvlib, coalescedNodes, frozenlist, graph, freezeworklist):
        u = spillworklist.pop(0)
        simplifyworklist.append(u)
        for m in movelist[u]:
            if m in activemMove or m in mvlib:
                x, y = m[0], m[1]
                if self.alias(coalescedNodes, y) == self.alias(coalescedNodes, u):
                    v = self.alias(coalescedNodes, x)
                else:
                    v = self.alias(coalescedNodes, y)
                activemMove.remove(m)
                frozenlist.append(m)
                if v in graph:
                    degree = len(graph[v])
                else:
                    degree = 0
                if self.mvrelated(v, movelist, activemMove, mvlib) and degree < len(reg2use):
                    freezeworklist.remove(v)
                    if v not in simplifyworklist:
                        simplifyworklist.append(v)

    def Assigncolors(self, selectStack, origingraph, coalescedNodes):
        coloredNode = {}
        spilledNode = []
        while len(selectStack) > 0:
            n = selectStack.pop()
            color = set(range(len(reg2use)))
            if n not in origingraph:
                origingraph[n] = set()
            for w in origingraph[n]:
                alias = self.alias(coalescedNodes, w)
                if alias in coloredNode:
                    color.discard(coloredNode[alias])
                elif alias in reg2use:
                    color.discard(reg2use.index(alias))
            if len(color) == 0:
                spilledNode.append(n)
            else:
                color = list(color)
                color.sort()
                coloredNode[n] = color.pop(0)
        for node in coalescedNodes:
            alias = self.alias(coalescedNodes, node)
            if alias in reg2use:
                coloredNode[node] = reg2use.index(alias)
            else:
                coloredNode[node] = coloredNode[alias]
        return coloredNode, spilledNode

    def ReWrite(self, spilledNode, irfunction):
        while len(spilledNode) > 0:
            node = spilledNode.pop(0)
            self.spillnum += 1
            addr = -4 * (self.spillnum + self.needra)
            for label in irfunction:
                linenum = []
                for i in range(len(label)):
                    smt = label[i]
                    if node in smt:
                        linenum.append(i)
                while len(linenum) > 0:
                    line = linenum.pop()
                    smt = label[line]
                    if smt[0] == lrEnum.mv:
                        if node == smt[1]:
                            varname = f"temp_{self.varnum}"
                            self.varnum += 1
                            smt[1] = varname
                            label.insert(line + 1, [lrEnum.sw, varname, addr, 'sp'])
                        if node == smt[2]:
                            varname = f"temp_{self.varnum}"
                            self.varnum += 1
                            smt[2] = varname
                            label.insert(line, [lrEnum.lw, varname, addr, 'sp'])
                    elif smt[0] == lrEnum.lw:
                        if node == smt[1]:
                            varname = f"temp_{self.varnum}"
                            self.varnum += 1
                            smt[1] = varname
                            label.insert(line + 1, [lrEnum.sw, varname, addr, 'sp'])
                        if node == smt[3]:
                            varname = f"temp_{self.varnum}"
                            self.varnum += 1
                            smt[3] = varname
                            label.insert(line, [lrEnum.lw, varname, addr, 'sp'])
                    elif smt[0] == lrEnum.binary:
                        if node == smt[2]:
                            varname = f"temp_{self.varnum}"
                            self.varnum += 1
                            smt[2] = varname
                            label.insert(line + 1, [lrEnum.sw, varname, addr, 'sp'])
                        if node == smt[3]:
                            varname = f"temp_{self.varnum}"
                            self.varnum += 1
                            smt[3] = varname
                            label.insert(line, [lrEnum.lw, varname, addr, 'sp'])
                        if node == smt[4]:
                            varname = f"temp_{self.varnum}"
                            self.varnum += 1
                            smt[4] = varname
                            label.insert(line, [lrEnum.lw, varname, addr, 'sp'])
                    elif smt[0] == lrEnum.li:
                        varname = f"temp_{self.varnum}"
                        self.varnum += 1
                        smt[1] = varname
                        label.insert(line + 1, [lrEnum.sw, varname, addr, 'sp'])
                    elif smt[0] == lrEnum.sw:
                        if node == smt[1]:
                            varname = f"temp_{self.varnum}"
                            self.varnum += 1
                            smt[1] = varname
                            label.insert(line, [lrEnum.lw, varname, addr, 'sp'])
                        if node == smt[3]:
                            varname = f"temp_{self.varnum}"
                            self.varnum += 1
                            smt[3] = varname
                            label.insert(line, [lrEnum.lw, varname, addr, 'sp'])
                    elif smt[0] == lrEnum.lui:
                        varname = f"temp_{self.varnum}"
                        self.varnum += 1
                        smt[1] = varname
                        label.insert(line + 1, [lrEnum.sw, varname, addr, 'sp'])
                    elif smt[0] == lrEnum.icmp:
                        if node == smt[2]:
                            varname = f"temp_{self.varnum}"
                            self.varnum += 1
                            smt[2] = varname
                            label.insert(line + 1, [lrEnum.sw, varname, addr, 'sp'])
                        if node == smt[3]:
                            varname = f"temp_{self.varnum}"
                            self.varnum += 1
                            smt[3] = varname
                            label.insert(line, [lrEnum.lw, varname, addr, 'sp'])
                    elif smt[0] == lrEnum.bnez:
                        varname = f"temp_{self.varnum}"
                        self.varnum += 1
                        smt[1] = varname
                        label.insert(line, [lrEnum.lw, varname, addr, 'sp'])
                    elif smt[0] == lrEnum.binaryi:
                        if node == smt[2]:
                            varname = f"temp_{self.varnum}"
                            self.varnum += 1
                            smt[2] = varname
                            label.insert(line + 1, [lrEnum.sw, varname, addr, 'sp'])
                        if node == smt[3]:
                            varname = f"temp_{self.varnum}"
                            self.varnum += 1
                            smt[3] = varname
                            label.insert(line, [lrEnum.lw, varname, addr, 'sp'])

    def writefunction(self, output, funcname, function, coloredNode, coalescedNodes):
        output.write(f"\t.globl {funcname}\n{funcname}:\t\t# @{funcname}\n")
        sp = 0
        save = []
        sp = self.needra + self.spillnum + self.funcarg
        temp = set()
        for reg in coloredNode:
            if reg not in reg2use and reg2use[coloredNode[reg]] in callee:
                temp.add(coloredNode[reg])
        sp += len(temp)
        sp = 4 * ((sp + 3) & ~3)
        save = list(temp)
        if sp != 0:
            output.write(f"\taddi\tsp,\tsp,\t{-sp}\n")
        if self.needra:
            output.write(f"\tsw\tra\t{sp - 4}(sp)\n")
        for reg in range(len(save)):
            output.write(f"\tsw\t{reg2use[save[reg]]}\t{sp - 4 * (self.needra + self.spillnum) - 4 * (reg + 1)}(sp)\n")
        for label in function:
            for smt in label:
                if smt[0] == lrEnum.mv:
                    x, y = self.alias(coalescedNodes, smt[1]), self.alias(coalescedNodes, smt[2])
                    if x == y:
                        pass
                    else:
                        output.write(f"\tmv\t{reg2use[coloredNode[x]]},\t{reg2use[coloredNode[y]]}\n")
                elif smt[0] == lrEnum.lw:
                    x, y = self.alias(coalescedNodes, smt[1]), self.alias(coalescedNodes, smt[3])
                    if y == 'sp':
                        output.write(f"\tlw\t{reg2use[coloredNode[x]]},\t{sp + smt[2]}(sp)\n")
                    else:
                        output.write(f"\tlw\t{reg2use[coloredNode[x]]},\t{smt[2]}({reg2use[coloredNode[y]]})\n")
                elif smt[0] == lrEnum.label:
                    output.write(f".{smt[1]}.{smt[2]}:\n")
                elif smt[0] == lrEnum.binary:
                    x, y, z = self.alias(coalescedNodes, smt[2]), self.alias(coalescedNodes, smt[3]), self.alias(coalescedNodes, smt[4])
                    output.write(f"\t{smt[1]}\t{reg2use[coloredNode[x]]},\t{reg2use[coloredNode[y]]},\t{reg2use[coloredNode[z]]}\n")
                elif smt[0] == lrEnum.li:
                    x = self.alias(coalescedNodes, smt[1])
                    output.write(f"\tli\t{reg2use[coloredNode[x]]}\t{smt[2]}\n")
                elif smt[0] == lrEnum.ret:
                    if self.needra:
                        output.write(f"\tlw\tra,\t{sp - 4}(sp)\n")
                    for reg in range(len(save)):
                        output.write(f"\tlw\t{reg2use[save[reg]]},\t{sp - 4 * (self.needra + self.spillnum) - 4 * (reg + 1)}(sp)\n")
                    if sp != 0:
                        output.write(f"\taddi\tsp,\tsp,\t{sp}\n")
                    output.write(f"\tret\n")
                elif smt[0] == lrEnum.call:
                    output.write(f"\tcall\t{smt[1]}\n")
                elif smt[0] == lrEnum.sw:
                    x, y = self.alias(coalescedNodes, smt[1]), self.alias(coalescedNodes, smt[3])
                    if y == 'sp':
                        output.write(f"\tsw\t{reg2use[coloredNode[x]]},\t{sp + smt[2]}(sp)\n")
                    elif y == 'arg':
                        output.write(f"\tsw\t{reg2use[coloredNode[x]]},\t{smt[2]}(sp)\n")
                    else:
                        output.write(f"\tsw\t{reg2use[coloredNode[x]]},\t{smt[2]}({reg2use[coloredNode[y]]})\n")
                elif smt[0] == lrEnum.lui:
                    x = self.alias(coalescedNodes, smt[1])
                    output.write(f"\tlui\t{reg2use[coloredNode[x]]}\t%hi({smt[2]})\n")
                elif smt[0] == lrEnum.icmp:
                    x, y = self.alias(coalescedNodes, smt[2]), self.alias(coalescedNodes, smt[3])
                    output.write(f"\t{smt[1]}\t{reg2use[coloredNode[x]]},\t{reg2use[coloredNode[y]]}\n")
                elif smt[0] == lrEnum.j:
                    output.write(f"\tj\t.{smt[1]}.{smt[2]}\n")
                elif smt[0] == lrEnum.bnez:
                    x = self.alias(coalescedNodes, smt[1])
                    output.write(f"\tbnez\t{reg2use[coloredNode[x]]},\t.{smt[2]}.{smt[3]}\n")
                elif smt[0] == lrEnum.binaryi:
                    x, y = self.alias(coalescedNodes, smt[2]), self.alias(coalescedNodes, smt[3])
                    if smt[1] == 'subi':
                        output.write(f"\taddi\t{reg2use[coloredNode[x]]},\t{reg2use[coloredNode[y]]},\t{-smt[4]}\n")
                    else:
                        output.write(f"\t{smt[1]}\t{reg2use[coloredNode[x]]},\t{reg2use[coloredNode[y]]},\t{smt[4]}\n")
            output.write('\n')

    def writeglobalvar(self, output, array):
        if array[0] == llvmEnum.GlobalVar:
            if type(array[3]).__name__ == 'str' and array[3][0] == '@':
                output.write(f'.{array[1]}:\n')
                output.write(f'\t.word {array[3][1:]}\n')
            elif array[3] == 'null':
                output.write(f'.{array[1]}:\n')
                output.write(f'\t.word 0\n')
            else:
                output.write(f'.{array[1]}:\n')
                output.write(f'\t.word {array[3]}\n')
        elif array[0] == llvmEnum.GlobalString:
            if array[2] == 1:
                output.write(f'.string.{array[1]}:\n')
                output.write(f'\t.zero 1\n')
            else:
                output.write(f'.string.{array[1]}:\n')
                output.write(f'\t.asciz \"{array[3]}\"\n')
        else:
            pass

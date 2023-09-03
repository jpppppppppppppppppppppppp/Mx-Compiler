from classEnum import *


class mem2reg:
    def __init__(self):
        self.next = {}
        self.pre = {}
        self.blocks = {}
        self.used = {}
        self.defd = {}
        self.allocavar = []

    def run(self, allfunc):
        ret = {}
        for func in allfunc:
            ret[func] = self.opt(allfunc[func])
        return ret

    def opt(self, function):
        self.next.clear()
        self.pre.clear()
        self.blocks.clear()
        self.used.clear()
        self.defd.clear()
        self.allocavar.clear()
        typelist = {}
        for block in function[2]:
            end = False
            nowlabel = block[0][1]
            if nowlabel not in self.next:
                self.next[nowlabel] = []
            if nowlabel not in self.pre:
                self.pre[nowlabel] = []
            self.blocks[nowlabel] = block
            for i in range(len(block)):
                smt = block[i]
                if end:
                    smt[0] = llvmEnum.Pass
                    continue
                if smt[0] == llvmEnum.Jump:
                    self.next[nowlabel].append(smt[1])
                    if smt[1] not in self.pre:
                        self.pre[smt[1]] = []
                    self.pre[smt[1]].append(nowlabel)
                    end = True
                elif smt[0] == llvmEnum.Br:
                    self.next[nowlabel].append(smt[2])
                    if smt[2] not in self.pre:
                        self.pre[smt[2]] = []
                    self.pre[smt[2]].append(nowlabel)
                    self.next[nowlabel].append(smt[3])
                    if smt[3] not in self.pre:
                        self.pre[smt[3]] = []
                    self.pre[smt[3]].append(nowlabel)
                    if smt[1] not in self.used:
                        self.used[smt[1]] = []
                    self.used[smt[1]].append([nowlabel, i])
                    end = True
                elif smt[0] == llvmEnum.Return:
                    if smt[2] not in self.used:
                        self.used[smt[2]] = []
                    self.used[smt[2]].append([nowlabel, i])
                    end = True
                elif smt[0] == llvmEnum.ReturnVoid:
                    end = True
                elif smt[0] == llvmEnum.Alloca:
                    typelist[smt[1]] = smt[2]
                    if smt[1] not in self.allocavar:
                        self.allocavar.append(smt[1])
                    if smt[1] not in self.defd:
                        self.defd[smt[1]] = {}
                    self.defd[smt[1]][nowlabel] = ['alloca', i]
                elif smt[0] == llvmEnum.Load:
                    if smt[3] not in self.used:
                        self.used[smt[3]] = []
                    self.used[smt[3]].append([nowlabel, i])
                elif smt[0] == llvmEnum.Getelementptr1:
                    if smt[3] not in self.used:
                        self.used[smt[3]] = []
                    self.used[smt[3]].append([nowlabel, i])
                    if smt[4] not in self.used:
                        self.used[smt[4]] = []
                    self.used[smt[4]].append([nowlabel, i])
                elif smt[0] == llvmEnum.Getelementptr2:
                    if smt[3] not in self.used:
                        self.used[smt[3]] = []
                    self.used[smt[3]].append([nowlabel, i])
                    if smt[4] not in self.used:
                        self.used[smt[4]] = []
                    self.used[smt[4]].append([nowlabel, i])
                elif smt[0] == llvmEnum.Trunc:
                    if smt[2] not in self.used:
                        self.used[smt[2]] = []
                    self.used[smt[2]].append([nowlabel, i])
                elif smt[0] == llvmEnum.Zext:
                    if smt[2] not in self.used:
                        self.used[smt[2]] = []
                    self.used[smt[2]].append([nowlabel, i])
                elif smt[0] == llvmEnum.Phi:
                    for use in smt[3]:
                        if use[0] not in self.used:
                            self.used[use[0]] = []
                        self.used[use[0]].append([nowlabel, i])
                elif smt[0] == llvmEnum.Icmp:
                    if smt[4] not in self.used:
                        self.used[smt[4]] = []
                    self.used[smt[4]].append([nowlabel, i])
                    if smt[5] not in self.used:
                        self.used[smt[5]] = []
                    self.used[smt[5]].append([nowlabel, i])
                elif smt[0] == llvmEnum.Store:
                    if smt[2] not in self.used:
                        self.used[smt[2]] = []
                    self.used[smt[2]].append([nowlabel, i])
                    if smt[3] not in self.defd:
                        self.defd[smt[3]] = {}
                    self.defd[smt[3]][nowlabel] = [smt[2], i]
                elif smt[0] == llvmEnum.Binary:
                    if smt[4] not in self.used:
                        self.used[smt[4]] = []
                    self.used[smt[4]].append([nowlabel, i])
                    if smt[5] not in self.used:
                        self.used[smt[5]] = []
                    self.used[smt[5]].append([nowlabel, i])
                elif smt[0] == llvmEnum.FuncCall:
                    for arg in smt[4]:
                        if arg[1] not in self.used:
                            self.used[arg[1]] = []
                        self.used[arg[1]].append([nowlabel, i])
                elif smt[0] == llvmEnum.FuncVoid:
                    for arg in smt[2]:
                        if arg[1] not in self.used:
                            self.used[arg[1]] = []
                        self.used[arg[1]].append([nowlabel, i])
        d = {}
        for label in self.blocks:
            d[label] = set()
            for labels in self.blocks:
                d[label].add(labels)
        while True:
            update = False
            for label in d:
                newd = set()
                if len(self.pre[label]) != 0:
                    for temp in self.blocks:
                        newd.add(temp)
                for pre in self.pre[label]:
                    newd = newd.intersection(d[pre])
                newd.add(label)
                if newd == d[label]:
                    continue
                update = True
                d[label] = newd
            if not update:
                break
        df = {}
        for label in self.blocks:
            if label not in df:
                df[label] = set()
            for n in d[label]:
                for suc in self.next[label]:
                    if n not in d[suc] or n == suc:
                        if n not in df:
                            df[n] = set()
                        df[n].add(suc)
        phi = {}
        for vars in self.allocavar:
            for label in self.defd[vars]:
                source, line = self.defd[vars][label]
                for dfs in df[label]:
                    if dfs not in phi:
                        phi[dfs] = {}
                    if vars not in phi[dfs]:
                        phi[dfs][vars] = {}
        while True:
            update = False
            toadd = set()
            for label in phi:
                for dfs in df[label]:
                    if dfs not in phi:
                        toadd.add(dfs)
                        update = True
                    else:
                        for vars in phi[label]:
                            if vars not in phi[dfs]:
                                phi[dfs][vars] = {}
                                update = True
            for label in toadd:
                phi[label] = {}
            if not update:
                break

        dt = {}
        parent = {}
        queue = ['entry']
        while len(queue) != 0:
            front = queue.pop(0)
            dt[front] = []
            d.pop(front)
            for item in d:
                d[item].discard(front)
                if len(d[item]) == 1 and item not in queue:
                    queue.append(item)
                    dt[front].append(item)
                    parent[item] = front
        varbank = {'entry': {}}
        for _, arg in function[1]:
            varbank['entry'][arg] = arg
        temp = {}
        for label in phi:
            if label not in varbank:
                varbank[label] = {}
            for arg in phi[label]:
                if arg not in temp:
                    temp[arg] = 0
                varbank[label][arg] = f'%{arg[1:]}.{temp[arg]}'
                phi[label][arg]['name'] = f'%{arg[1:]}.{temp[arg]}'
                temp[arg] += 1
        task = ['entry']
        while len(task) > 0:
            self.rename(task, varbank, phi, df, parent, dt, typelist)
        self.next.clear()
        self.pre.clear()
        for block in function[2]:
            nowlabel = block[0][1]
            if nowlabel not in self.next:
                self.next[nowlabel] = []
            if nowlabel not in self.pre:
                self.pre[nowlabel] = []
            for i in range(len(block)):
                smt = block[i]
                if smt[0] == llvmEnum.Jump:
                    self.next[nowlabel].append(smt[1])
                    if smt[1] not in self.pre:
                        self.pre[smt[1]] = []
                    self.pre[smt[1]].append(nowlabel)
                elif smt[0] == llvmEnum.Br:
                    self.next[nowlabel].append(smt[2])
                    if smt[2] not in self.pre:
                        self.pre[smt[2]] = []
                    self.pre[smt[2]].append(nowlabel)
                    self.next[nowlabel].append(smt[3])
                    if smt[3] not in self.pre:
                        self.pre[smt[3]] = []
                    self.pre[smt[3]].append(nowlabel)
                    if smt[1] not in self.used:
                        self.used[smt[1]] = []
                    self.used[smt[1]].append([nowlabel, i])
        todel = []
        for block in self.blocks:
            if block not in self.pre or len(self.pre[block]) == 0 and block != 'entry':
                todel.append(block)
        for label in phi:
            for var in phi[label]:
                res = [llvmEnum.Phi, phi[label][var]['name'], typelist[var], []]
                for source in phi[label][var]:
                    if source in todel:
                        continue
                    if source not in ['name', 'type']:
                        res[-1].append([phi[label][var][source], source])
                self.blocks[label].insert(1, res)
        for todo in todel:
            for i in range(len(function[2])):
                if function[2][i][0][1] == todo:
                    function[2].pop(i)
                    break
        return dt
    def rename(self, task, varbank, phi, df, parent, dt, typelist):
        label = task.pop(0)
        if label not in varbank:
            varbank[label] = {}
        for i in range(len(self.blocks[label])):
            ins = self.blocks[label][i]
            if ins[0] == llvmEnum.Alloca:
                ins[0] = llvmEnum.Pass
                varbank[label][ins[1]] = '0'
            elif ins[0] == llvmEnum.Load:
                if ins[3] in self.allocavar:
                    ins[0] = llvmEnum.Pass
                    varbank[label][ins[1]] = self.getvalue(label, parent, varbank, ins[3])
                else:
                    varbank[label][ins[1]] = ins[1]
            elif ins[0] == llvmEnum.Return:
                ins[2] = self.getvalue(label, parent, varbank, ins[2])
            elif ins[0] == llvmEnum.Getelementptr1:
                varbank[label][ins[1]] = ins[1]
                ins[3] = self.getvalue(label, parent, varbank, ins[3])
                ins[4] = self.getvalue(label, parent, varbank, ins[4])
            elif ins[0] == llvmEnum.Getelementptr2:
                varbank[label][ins[1]] = ins[1]
                ins[3] = self.getvalue(label, parent, varbank, ins[3])
                ins[4] = self.getvalue(label, parent, varbank, ins[4])
            elif ins[0] == llvmEnum.Trunc:
                varbank[label][ins[1]] = ins[1]
                ins[2] = self.getvalue(label, parent, varbank, ins[2])
            elif ins[0] == llvmEnum.Zext:
                varbank[label][ins[1]] = ins[1]
                ins[2] = self.getvalue(label, parent, varbank, ins[2])
            elif ins[0] == llvmEnum.Br:
                ins[1] = self.getvalue(label, parent, varbank, ins[1])
            elif ins[0] == llvmEnum.Phi:
                varbank[label][ins[1]] = ins[1]
                for use in ins[3]:
                    todo = self.getvalue(label, parent, varbank, use[0])
                    if todo != None:
                        use[0] = todo
            elif ins[0] == llvmEnum.Icmp:
                varbank[label][ins[1]] = ins[1]
                ins[4] = self.getvalue(label, parent, varbank, ins[4])
                ins[5] = self.getvalue(label, parent, varbank, ins[5])
            elif ins[0] == llvmEnum.Store:
                todo = self.getvalue(label, parent, varbank, ins[2])
                if todo != None:
                    varbank[label][ins[3]] = todo
                    ins[2] = todo
                else:
                    varbank[label][ins[3]] = ins[2]
                if ins[3] in self.allocavar:
                    ins[0] = llvmEnum.Pass
            elif ins[0] == llvmEnum.Binary:
                varbank[label][ins[1]] = ins[1]
                ins[4] = self.getvalue(label, parent, varbank, ins[4])
                ins[5] = self.getvalue(label, parent, varbank, ins[5])
            elif ins[0] == llvmEnum.FuncCall:
                varbank[label][ins[1]] = ins[1]
                for arg in ins[4]:
                    todo = self.getvalue(label, parent, varbank, arg[1])
                    if todo != None:
                        arg[1] = todo
            elif ins[0] == llvmEnum.FuncVoid:
                for arg in ins[2]:
                    todo = self.getvalue(label, parent, varbank, arg[1])
                    if todo != None:
                        arg[1] = todo
        for next in self.next[label]:
            if next in phi:
                for var in phi[next]:
                    todo = self.getvalue(label, parent, varbank, var)
                    if todo == None:
                        if typelist[var] == 'ptr':
                            phi[next][var][label] = 'null'
                        else:
                            phi[next][var][label] = '0'
                    else:
                        phi[next][var][label] = todo
        for child in dt[label]:
            task.append(child)

    def getvalue(self, label, parent, varbank, varname):
        while True:
            if varname.isdigit() or varname[1:].isdigit():
                return varname
            if varname in varbank[label]:
                return varbank[label][varname]
            if label in parent:
                label = parent[label]
                continue
            if varname in ['true', 'false', 'null']:
                return varname
            if varname[0] == '@':
                return varname
            return None

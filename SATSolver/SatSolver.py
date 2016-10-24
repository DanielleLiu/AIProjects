#Author: Shuqi Liu.
# SATSolver implemented with WalkSAT and DPLL.
# The functions that generated the experimental data include: testDPLL() that calls DPLL and its related helper functions,
# and testWalkSat that calls walkSat and its related helper functions.
# The data is output to text files: dataDPLL.txt and dataWalkSAT.txt
import glob,time,random


 #TODO: speed-up; keep index/hash of unknwon clauses, pointer to clauses with certian symbol - pure symbol and flip check only those
def walkSat(clauses,symbols,maxFlips,clauseNum):
    model = [True if random.randint(0, 1) == 1 else False for s in symbols]
    maxSatisfied = 0
    for i in range(maxFlips):
        trueClauses = 0
        falseClauses =[]
        for c in clauses:
            if evaluateWalk (c,model): trueClauses+=1
            else: falseClauses.append(c) #always select the first false #TODO: change to actual random selection
        if (trueClauses == clauseNum): #always pass all clauses in, always complete
            # print "Assignment",model
            return (True,model,i)
        if (trueClauses>maxSatisfied): maxSatisfied = trueClauses
        clause = random.choice(falseClauses)
        prob = random.randint(0,1)
        if prob ==1:
            c = random.choice(clause) #a string of 1 symbol
            model[abs(c)-1] = not model[abs(c)-1] #want to change the model
        else: #todo: how to select the max satisfying symbol efficiently
            satisfied = []
            for currS in clause:
                currmodel = model[:] #when finding the most helpful symbol, DN want to change the actual model yet
                currmodel[abs(currS)-1]= not currmodel[abs(currS)-1]
                currSatisfied = 0
                for c in clauses:
                    if evaluateWalk(c,currmodel): currSatisfied+=1
                satisfied.append(currSatisfied)
            symbol = clause[satisfied.index(max(satisfied))]
            model [abs(symbol)-1] = not model[abs(symbol)-1]
    print "Unsatisfiable within given max number of iterations", maxFlips
    print "MaxClauseSatisfied: ", maxSatisfied
    return (False,maxSatisfied,i)

def evaluateWalk(clause,model):
    for c in clause:
        currVal = model[abs(c)-1]
        if c<0: currVal = not currVal
        if currVal: return True
    return False

def DPLL(clauses,symbols,model):
    trueClauses = 0
    unsatisfiedClauses = []
    for c in clauses:
        if evaluate(c,model) is None: unsatisfiedClauses.append(c) #exists at least one unknown pass
        elif not evaluate(c,model):return False #exists at least one known false, return false
        else: trueClauses+=1
    if (trueClauses == len(clauses)):
        print "Assignment",model
        return True
    (p,value) = findPure(symbols,unsatisfiedClauses)
    if p is not None:
        rest = symbols[:]
        rest.remove(p)  # return None; very original symbols list should remain unchanged.
        newmodel1 = model.copy()
        newmodel1[p] = value #abs,int as the key
        return DPLL(unsatisfiedClauses,rest,newmodel1) #pass only unsatisfied - clauses containing the pure symbol
    (p, value) = findUnit(unsatisfiedClauses,model)
    if p is not None:
        rest = symbols[:]
        rest.remove(p)  # return None; very original symbols should remain unchanged?
        newmodel1 = model.copy()
        newmodel1[p] = value # p is always postive int form
        return DPLL(unsatisfiedClauses,rest,newmodel1) # pass only unsatisfied - the current unit clause

    # #branching
    p = symbols[0] #get to this step last time when len(symbols)==1; next time, rest = 0; will return true
    rest = symbols[:]
    rest.remove(p) #return None; very original symbols should remain unchanged?
    newmodel1 = model.copy()
    newmodel2 = model.copy()
    newmodel1[p] = True
    newmodel2[p] = False
    return DPLL(unsatisfiedClauses,rest,newmodel1) or DPLL(unsatisfiedClauses,rest,newmodel2)

#changes dynamically, as value being assigned; TODO: remove the unit clause found immediately
def findUnit(clauses,model): #always return the pos int symbol, and the value
    for clause in clauses:
        if len(clause) ==1:
            return abs(c[0]),c>0 #return the symbol as pos integer and value
        assigned=0
        for c in clause:
            if model.has_key(abs(c)):assigned+=1
            else: symbol = c
        if (assigned == len(clause)-1):
            return abs(symbol),symbol>0
    return (None,None)

#TODO: possibily find all pure symbols in the pure set and set the values for all; remove all the clauses containing the pure symbol
def findPure(symbols,clauses): #return the symbol in pos int form and its value
    pure=set() #set of pos or neg symbols in the clauses
    for clause in clauses:
        for c in clause:
            pure.add(c)
    for s in symbols:
        if (s in pure) and ((-s) not in pure): return (s,True) #only positive form
        if (s not in pure) and ((-s) in pure): return (s, False) #pure ontly negative form
    return (None, None)

def evaluate (clause,model):
    false = 0
    for c in clause: # ensure going to this for loop atleast once
        if model.has_key(abs(c)): #key is in string format; only set values will be checked; if all None, leave the result as None; if anyone true, change
            value = model[abs(c)]
            if c <0: value = not value
            if value:  return True
            else: false+=1
    if false == len(clause): return False
    return None

def readOne(filename):
    f = open(filename)
    d = f.readlines() # TODO: change to read(), then split at 0
    f.close()

    startLine = 0
    variablesNum = 0
    for i in d:
        startLine += 1
        if i[0]=='c':
            continue
        if i[0]=='p':
            info = i.split()
            clauseNum = int(info[3])
            variablesNum = int(info[2])
            break
    model = {} #leave the 0 position as none #list of dictionary?
    symbols = [i+1 for i in range (variablesNum)] #list of integers
    clauses = []
    for i in d[startLine:]:
        if i [0]=='c':
            continue
        clauses.append(map(int,i.split()[:-1]))
    return clauses,model,symbols,clauseNum


files = glob.glob("A3Formulas/*.cnf")
# files = glob.glob("tests/*.cnf")
def testDPLL(files):
    fout = open("dataDPLL.txt",'a')
    for f in files:
        clauses, model, symbols, clauseNum = readOne(f)
        print "\n",f
        start_time = time.time()
        result =  DPLL(clauses,symbols,model)
        print result
        satisfiability = 's' if result else 'u'
        assert (f[-5]==satisfiability),"------Wrong solution found!!!------"
        t = time.time()-start_time
        print t
        fout.write(str(f)+" "+str(result)+"  "+str(t)+"\n")
    fout.close()

def testWalkSat(files):
    fout = open("dataWalkSAT1.txt",'a')
    for f in files:
        clauses, model, symbols, clauseNum = readOne(f)
        print "\n",f
        for i in range(10):
            start_time = time.time()
            result =  walkSat(clauses,symbols,5000,clauseNum)
            print result
            satisfiability = 's' if result[0] else 'u'
            assert (f[-5]==satisfiability),"------Wrong solution found!!!------"
            t =  time.time()-start_time
            print t
            if result[0]: fout.write(str(f)+" "+str(result[0])+"  "+str(t)+"   "+str(result[2])+"\n") #file,T/F,time,FlipsUsed
            else: fout.write(str(f)+" "+str(result[0])+"  "+str(t)+" "+str(result[1])+"\n") #file, T/F, time, maxSatisfied when quit
    fout.close()

testDPLL(files)
testWalkSat(files)
import glob,time,random

"""
pure symbols? always the same, find once and assigned once at the beginning?
remaining value DN need to be assigned, randomly assign one at the end? before return?
random? call random.randint each time or generate a list of random numbers and select
"""

def walkSat(clauses,symbols,maxFlips,clauseNum):
    model={}
    for s in symbols:
        prob = random.randint(0,1)
        if prob == 0: model[s] = False
        else: model[s]=True
    for i in range(maxFlips):
        trueClauses = 0
        for c in clauses:
            if evaluate (c,model): trueClauses+=1
            else: clause = c #always select the first false #TODO: change to actual random selection
        if (trueClauses == clauseNum): #always pass all clauses in, always complete
            print "Assignment",model
            return True#,model
        #index = random.randint(0,clauseNum-1)
        prob = random.randint(0,1)
        if prob ==1:
            c = random.choice(clause) #a string of 1 symbol
            model[abs(eval(c))] = not model[abs(eval(c))] #want to change the model
        else: #todo: how to select the max satisfying symbol efficiently
            satisfied = []
            for currS in clause:
                currmodel = model.copy() #when finding the most helpful symbol, DN want to change the actual model yet
                currmodel[abs(eval(currS))]= not currmodel[abs(eval(currS))]
                currSatisfied = 0
                for c in clauses:
                    if evaluate(c,currmodel): currSatisfied+=1
                satisfied.append(currSatisfied)
            symbol = clause[satisfied.index(max(satisfied))]
            model [abs(eval(symbol))] = not model[abs(eval(symbol))]
    return False




def DPLL(clauses,symbols,model):
    trueClauses = 0
    for c in clauses:
        if evaluate(c,model) is None: break #exists at least one unknown pass
        elif not evaluate(c,model):return False #exists at least one known false, return false
        else: trueClauses+=1
    if (trueClauses == len(clauses)):
        print "Assignment",model
        return True # alternative, if is None, call another function to do remaining
    (p,value) = findPure(symbols,clauses)
    if p is not None:
        rest = symbols[:]
        rest.remove(p)  # return None; very original symbols should remain unchanged?
        newmodel1 = model.copy()
        newmodel1[p] = value #abs,int as the key
        return DPLL(clauses,rest,newmodel1)
    (p, value) = findUnit(clauses,model)
    if p is not None:
        rest = symbols[:]
        rest.remove(p)  # return None; very original symbols should remain unchanged?
        newmodel1 = model.copy()
        newmodel1[p] = value # p is always postive int form
        return DPLL(clauses,rest,newmodel1)

    # #branching
    p = symbols[0] #get to this step last time when len(symbols)==1; next time, rest = 0; will return true
    rest = symbols[:]
    rest.remove(p) #return None; very original symbols should remain unchanged?
    newmodel1 = model.copy()
    newmodel2 = model.copy()
    newmodel1[p] = True
    newmodel2[p] = False
    return DPLL(clauses,rest,newmodel1) or DPLL(clauses,rest,newmodel2)

#changes dynamically, as value being assigned
def findUnit(clauses,model): #always return the pos int symbol, and the value
    for clause in clauses:
        if len(clause) ==1:
            return abs(eval(c[0])),eval(c)>0 #return the symbol as pos integer and value
        if evaluate(clause,model): continue
        assigned=0
        for c in clause:
            if model.has_key(abs(eval(c))):assigned+=1
            else: symbol = eval(c)
        if (assigned == len(clause)-1):
            return abs(symbol),symbol>0
    return (None,None)

#always the same; only need to find once, put in a list; possibly assign all value once?
def findPure(symbols,clauses): #return the symbol in pos int form and its value
    pure=set() #set of pos or neg symbols in the clauses
    for clause in clauses:
        for c in clause:
            if eval(c) not in pure: pure.add(eval(c))
    for s in symbols:
        if (s in pure) and ((-s) not in pure): return (s,True) #only positive form
        if (s not in pure) and ((-s) in pure): return (s, False) #pure ontly negative form
    return (None, None)


#evaluate one clause; if at least one True return True, if all F return False, else return None
def evaluate (clause,model):
    false = 0
    # if all None, return None; if any True, return True; if all False, return False; otherwise, None
    for c in clause: # ensure going to this for loop atleast once
        key = abs(eval(c))
        if model.has_key(key): #key is in string format; only set values will be checked; if all None, leave the result as None; if anyone true, change
            value = model[key]
            if eval(c) <0: value = not value
            if value:  return True
            else: false+=1
    if false == len(clause): return False
    return None
     # if a clause gets longer, put an if into the for loop so that when false leave early --won't know early as it's or statement
    #if everything is None, result = None; else change to a true of false case

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
        # print i
        if i [0]=='c':
            continue
        clauses.append(i.split()[:-1]) #TODO: a list of string format -- decide eval to list of int or no?
    return clauses,model,symbols,clauseNum

#start_time = time.time()
files = glob.glob("A3Formulas/*.cnf")
# files = glob.glob("tests/*.cnf")
for f in files:
    start_time = time.time()
    clauses, model, symbols, clauseNum = readOne(f)
    print "\n",f
    # print clauses,'\n',model,'\n',symbols
    # print DPLL(clauses,symbols,model)
    result =  walkSat(clauses,symbols,1500,clauseNum)
    print result
    satisfiability = 's' if result else 'u'
    assert (f[-5]==satisfiability),"------Wrong solution found!!!------"
    print time.time()-start_time
# print time.time()-start_time


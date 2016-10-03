import glob,time

def DPLL(clauses,symbols,model):
    trueClauses = 0
    for c in clauses:
        if evaluate(c,model) is None: break #exists at least one unknown pass
        elif not evaluate(c,model):return False #exists at least one known false, return false
        else: trueClauses+=1
    if (trueClauses == len(clauses)):
        print "Assignment",model
        return True #alternative, if is None, call another function to do remaining
    (p,value) = findPure(symbols,clauses)
    if p is not None:
        rest = symbols[:]
        rest.remove(p)  # return None; very original symbols should remain unchanged?
        newmodel1 = model.copy()
        newmodel1[p] = value
        return DPLL(clauses,rest,newmodel1)
    (p, value) = findUnit(clauses)
    if p is not None:
        rest = symbols[:]
        rest.remove(p)  # return None; very original symbols should remain unchanged?
        newmodel1 = model.copy()
        newmodel1[p] = value
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

def findUnit(clauses):
    for c in clauses:
        if len(c) ==1:
            return c[0],eval(c)>0
    return (None,None)

def findPure(symbols,clauses):
    pure=set()
    for clause in clauses:
        for c in clause:
            # if (abs(eval(c)) in pure) and ((-eval(c)) in pure): continue
            if eval(c) not in pure: pure.add(eval(c))
    for s in symbols:
        if (abs(eval(c)) in pure) and ((-eval(c)) not in pure): return (s,True) #only positive form
        if (abs(eval(c)) not in pure) and ((-eval(c)) in pure): return (s, False) #pure ontly negative form
    return (None, None)


#if all symbols in one clauses evalutes to !=0 or to true
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
    # startLine = 0
    # variablesNum = 0
    info = d[0].split()
    clauseNum = int(info[3])
    variablesNum = int(info[2])

    # for i in d:
    #     if i[0]=='c':
    #         continue
    #     if i[0]=='p':
    #         print "Here"
    #         info = d[0].split()
    #         clauseNum = int(info[3])
    #         variablesNum = int(info[2])
    #         break
    #     startLine+=1
    model = {} #leave the 0 position as none #list of dictionary?
    symbols = [i+1 for i in range (variablesNum)]
    clauses = []
    for i in d[1:]:
        if i [0]=='c':
            continue
        clauses.append(i.split()[:-1]) #TODO: a list of string format -- decide eval to list of int or no?
    return clauses,model,symbols

start_time = time.time()
# files = glob.glob("A3Formulas/*.cnf")
files = glob.glob("tests/*.cnf")
print files
for f in files:
    print f
    clauses, model, symbols = readOne(f)
     # print clauses
    print "\n",f
    print DPLL(clauses,symbols,model)
print time.time()-start_time



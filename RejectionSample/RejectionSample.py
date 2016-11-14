# Author: Shuqi Liu. 11/12/2016.
# This program computes the probability of any give combination involving five events
# Events: B = Burglary, E= earthquake, A = alarm, J = JohnCalls, M= MaryCalls
# The query is given ghrough standard input following the format: bnet Af Bt given Jt
# We can query as many times as we want, until "quit" is typed.
import random

#find the assignment for an event with probability of True = p
def findP(p):
    if (random.random()<p): #generate a random number between [0,1)
        return True
    else:
        return False

#generate a random sample based on the probabilities (hard-coded)
def priorSample():
    B = 0.02
    E = 0.03
    A = [0.97,0.92,0.36,0.03] #TT.TF,FT,FF
    J = [0.85,0.07] #T,R
    M = [0.69,0.02] #T,R
    currB = findP(B)
    currE = findP(E)
    if (currB and currE):
        currA = findP(A[0])
    elif currB and (not currE):
        currA = findP(A[1])
    elif (not currB) and currE:
        currA = findP(A[2])
    else:
        currA = findP(A[3])
    if currA:
        currJ = findP(J[0])
        currM = findP(M[0])
    else:
        currJ = findP(J[1])
        currM = findP(M[1])
    dic = {'B':currB,'E':currE,'A':currA,'J':currJ,'M':currM} #sample recorded in a dictionary
    return dic

# evidence is a dictionary with key = variable name, value = T/F; sample is also a dictionary
def checkConsistency(evidence,sample):
    evi = evidence.keys()
    for e in evi:
        if (evidence[e]!=sample[e]): #not exclusive or, when differ a!=b evaluates to T corresponding to the situation: inconsisdent
           return False # get to this loop only when evidence[e] and sample[e] are different
    return True

def rejectionSample(query,evidence,trials):
    accepted = 0
    match = 0
    if bool(evidence): # evidence is not empty
        for t in range(trials):
            x = priorSample()
            # print t,x
            if checkConsistency(evidence,x):
                accepted +=1
                if checkConsistency(query,x):
                    match +=1
        return float(match)/accepted
    else: # evidence is empty
        for t in range(trials):
            x = priorSample()
            if checkConsistency(query, x):
                match += 1
        return float(match) / trials

#query: while true, keep asking for input
while True:
    input = raw_input("Your Query (type quit to quit querying): ")
    if (input=='quit'):
        print "Query Finished."
        break
    input = input.split('given')
    rawQuery = input[0].split()[1:]
    rawEvidence=[]
    if len(input) >1: rawEvidence = input[1].split()
    query={}
    evidence={}
    for q in rawQuery: #Does not sanitize input, assume everything is typed in the correct format
        query[q[0]] = (True if (q[1]=='t') else False)
    for e in rawEvidence:
        evidence[e[0]] = (True if(e[1]=='t') else False)
    # print query, evidence
    print rejectionSample(query,evidence,10000000)


# test runs
# print rejectionSample({'A':False,'B':True},{'M':False},10000000) #1
# print rejectionSample({'A':False,'E':True},{},10000000) #2
# print rejectionSample({'A':False,'J':True},{'B':True,'E':False},10000000) #0.0076; 3
# print rejectionSample({'B':True,'A':False,'M':False,'J':True,'E':True},{},10000000) #4
# print rejectionSample({'A':True},{'B':False,'E':False},10000) #1
# print rejectionSample({'A':True},{'B':True,'E':False},100000)
# print rejectionSample({'A':True},{'B':True,'E':True},100000)
# print rejectionSample({'A':True},{'B':False,'E':True},100000)
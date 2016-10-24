import itertools,os,shutil
import numpy as np

minisat = "/usr/local/bin/minisat"
class SudukuSolver():
    def __init__(self):
        # variableString = ["{:03x}".format(i, 'X') for i in xrange(0x000, 0x1000)]
        variableString = [i for i in range(int(0x000) + 1, int(0x1000) + 1)]
        self.allvars = np.array(variableString)
        self.allvars = self.allvars.reshape(16, 16, 16)

    def exactlyOne(self,vars,fout):
        #at least one
        fout.write("\n")
        for var in vars: #vars are a list of strings representing numbers
            fout.write(str(var)+"  ")
        fout.write("0")

        #at most one
        pairs = itertools.combinations(vars,2)
        for pair in pairs:
            fout.write("\n")
            for symbol in pair:
                fout.write("-" + str(symbol) + "  ")
            fout.write("0")

    def getUniformRules(self):
        fout = open("ruleUniform.cnf", 'w')
        fout.write("p cnf 4096 123904")
        for i in range(16): #exactly one per grid
            for j in range(16):
                self.exactlyOne(self.allvars[i,j,:],fout)

        for i in range(16): #rows unique rule
            for j in range(16):
                # row = self.allvars[i,:,j]
                self.exactlyOne(self.allvars[i,:,j],fout)

        for i in range(16): #column unique
            for j in range(16):
                self.exactlyOne(self.allvars[:,i,j],fout)#all grid for first row

        for i in range(4): #4X4 block unique rule
            for j in range(4):
                for k in range(16):
                    self.exactlyOne(np.hstack(self.allvars[4*i:4*(i+1),4*j:4*(j+1),k]),fout) # per block
        fout.close()

    def getOneGameRule(self,fgame):
        f = open(fgame)
        start = f.readlines()
        f.close()
        frule = fgame[:-4]+"rule.cnf"
        shutil.copyfile("ruleUniform.cnf", frule)

        f = open(frule,"a")
        row = -1
        clauses = 0
        for line in start: #a string of a line
            line = line.strip()
            row+=1
            col = -1
            for symbol in line:
                if symbol!=" ":
                    col+=1
                    if symbol!="_":
                        currVar = 16*16*row+16*col+int(symbol,16)+1
                        f.write("\n"+str(currVar)+"  0")
                        clauses +=1
        f.close()
        f = open(frule)
        d = f.readlines()
        f.close()
        headline = d[0].split()
        headline[-1]=str(int(headline[-1])+clauses)
        f = open(frule,'w')
        f.write(" ".join(headline)+"\n")
        for line in d[1:]:
            f.write(line)
        f.close()
        return frule

    def solve(self,fgame):
        fin = self.getOneGameRule(fgame)
        fout = fgame[:-4]+"sol.txt"
        os.system(minisat+" "+fin+" "+fout)
        f = open(fout)
        solution = f.readlines()
        f.close()
        if solution[0].startswith("UN"):
            print "Sorry. No Solution."
        else:
            assignment = solution[1].split()
            self.writeMapSolution(assignment,fout[:-4]+"Mapped.txt")
            self.checkUnique(assignment,fgame)
        return fout

    def checkUnique(self,assignment,fgame):
            assignment = map(int,assignment)
            newSol = [-x for x in assignment] #generate the asserstion that all assignment must different than current solution
            newSol = map(str,newSol)

            f = open(fgame[:-4] + "rule.cnf")
            d = f.readlines()
            f.close()
            #update headline clause number informations
            headline = d[0].split()
            headline[-1] = str(int(headline[-1]) + 1)
            d[0] = " ".join(headline) + "\n"
            fnewSol = fgame[:-4] + "ruleNewSol.cnf"
            f = open(fnewSol,'w')
            for i in d:
                f.write(i)
            f.write("\n"+"  ".join(newSol)) #write the new clause: assert a different solution
            f.close()

            foutNewSol=fgame[:-4]+"sol2.txt"
            os.system(minisat + " " + fnewSol + " " +foutNewSol)
            f = open(foutNewSol)
            solution = f.readlines()
            f.close()
            if solution[0].startswith("UN"):
                print "Solution is unique."
            else:
                assignment = solution[1].split()
                self.writeMapSolution(assignment, fgame[:-4]+"solMapped.txt")

#print the formated solution and write the solution to a text file
    def writeMapSolution(self,assignment,fname):
        f = open(fname,'a')
        f.write("\nA Solution:")
        for row in range(16):
            if (row%4==0):
                print ""
                f.write("\n")
            for col in range(16):
                if (col%4==0):
                    print " ",
                    f.write("   ")
                for entry in range(16):
                    curr = eval(assignment[16*16*row+16*col+entry])
                    if curr>0:
                        print hex(curr-1)[-1], #last digit in hex format
                        f.write(str(hex(curr-1)[-1])+" ")
                        break
            print ""
            f.write("\n")


temp = SudukuSolver()
# temp.getUniformRules()
temp.solve("SudokuPuzzles/prob_2.inp")
# temp.solve("SudokuPuzzles/test_empty.inp")
# temp.writeMapSolution("SudokuPuzzles/prob_2sol.txt")



"""height: numbers that could be put in this grid
#   1st dimension, all 16*16 slicings form rule for grid 000,001,002 [:,:,1]
#   rows: 000,010,020; 001,011,021....; 100,110,120; 101,111,121,...  3rd dimensions [0,:,0], for each contained list, 121 rules
#     columns: 000,100,200 [:,0,0]
#     1st dimension:

# 0-15,16-32; every 16 forms a rule for exactly 1 per grid; 4096/16 = 16*16 grids, 16nums per grid
# 1st of every 16 - a number each row, 2nd of every 16; a number each row - 16 per row then increment to next row
# every 1st of 16*16 - 16 number each column; repeat 16*16 times from 1st column and increment to all columns
# per 4X4:?"""
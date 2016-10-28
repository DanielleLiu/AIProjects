# Author: Shuqi Liu. 10/26/2016
# the SudukuSolver will read in a hex suduku in a text file,
# find the solution, print to the standard output and save it to a text file prob_#solMapped.txt
# if no solution, no file will be written and the "Sorry No Solution" message will be printed out
# if there are mutlile solutions, two solutions will be found, printed and saved to text file
# otherwise, the standard output will print unique solution
import itertools,os,shutil,glob
import numpy as np

minisat = "/usr/local/bin/minisat"
class SudukuSolver():
    def __init__(self):
        # variableString = ["{:03x}".format(i, 'X') for i in xrange(0x000, 0x1000)] enumerate in hex
        variableString = [i for i in range(int(0x000) + 1, int(0x1000) + 1)] #generate all the variables in integer format
        self.allvars = np.array(variableString)
        self.allvars = self.allvars.reshape(16, 16, 16) #put variables in a 16*16*16 matrix where index is [row,column,number at the grid]

    # general rule: at most one variable is True in the given vars list, write to output file: fout
    def atmostOne(self,vars,fout):
        pairs = itertools.combinations(vars,2)
        for pair in pairs:
            fout.write("\n")
            for symbol in pair:
                fout.write("-" + str(symbol) + "  ")
            fout.write("0")

    # general rule: at least one variable in the given vars list is true
    def atleastOne(self,vars,fout):
        fout.write("\n")
        for var in vars: #vars are a list of strings representing numbers
            fout.write(str(var)+"  ")
        fout.write("0")

    # general rule: exactly one variable in the given vars list is true
    def exactlyOne(self,vars,fout):
        self.atmostOne(vars,fout)
        self.atleastOne(vars,fout)

    # generate uniform rules: per grid, row, column and 4X4 box, output to ruleUniform1.cnf
    def getUniformRules(self):
        fout = open("ruleUniform1.cnf", 'w')
        fout.write("p cnf 4096 123136")
        for i in range(16): #exactly one per grid
            for j in range(16):
                self.exactlyOne(self.allvars[i,j,:],fout)

        for i in range(16): #rows unique rule
            for j in range(16):
                self.atmostOne(self.allvars[i,:,j],fout)

        for i in range(16): #column unique
            for j in range(16):
                self.atmostOne(self.allvars[:,i,j],fout)#all grid for first row

        for i in range(4): #4X4 block unique rule
            for j in range(4):
                for k in range(16):
                    self.atmostOne(np.hstack(self.allvars[4*i:4*(i+1),4*j:4*(j+1),k]),fout) # per block
        fout.close()
        
# alternative get uniform rule in 123,906 number of clauses
##    def getUniformRules(self):
##        fout = open("ruleUniform.cnf", 'w')
##        fout.write("p cnf 4096 123904")
##        for i in range(16): #exactly one per grid
##            for j in range(16):
##                self.exactlyOne(self.allvars[i,j,:],fout)
##
##        for i in range(16): #rows unique rule
##            for j in range(16):
##                # row = self.allvars[i,:,j]
##                self.exactlyOne(self.allvars[i,:,j],fout)
##
##        for i in range(16): #column unique
##            for j in range(16):
##                self.exactlyOne(self.allvars[:,i,j],fout)#all grid for first row
##
##        for i in range(4): #4X4 block unique rule
##            for j in range(4):
##                for k in range(16):
##                    self.exactlyOne(np.hstack(self.allvars[4*i:4*(i+1),4*j:4*(j+1),k]),fout) # per block
##        fout.close()

    # read the game set up from a text file fgame, output the specific rule for this game to fgame+rule.cnf
    def getOneGameRule(self,fgame):
        f = open(fgame)
        start = f.readlines()
        f.close()
        frule = fgame[:-4]+"rule.cnf"
        shutil.copyfile("ruleUniform1.cnf", frule) #copy the uniform rule to the output file

        f = open(frule,"a") #append the specific rule at the end of the uniform rule
        row = -1
        clauses = 0 # count total number of added clauses
        for line in start: #a string of a line in the setup text file
            line = line.strip()
            row+=1
            col = -1
            for symbol in line:
                if symbol!=" ": #ignore white space
                    col+=1
                    if symbol!="_":
                        currVar = 16*16*row+16*col+int(symbol,16)+1 #convert hex at specific position to corresponding binary variable integer
                        f.write("\n"+str(currVar)+"  0") #write the rule to the rule file
                        clauses +=1
        f.close()
        #adjust the headline to right number of clauses
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

    # check if the solution is unique
    def checkUnique(self,assignment,fgame):
            assignment = map(int,assignment)
            newSol = [-x for x in assignment] #generate the asserstion that all assignment must different than current solution
            newSol = map(str,newSol)
            #update the specific game rule file, append the new assertion
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
            # use miniSAT to find the solution and direct the result to game_#sol2.txt
            foutNewSol=fgame[:-4]+"sol2.txt"
            os.system(minisat + " " + fnewSol + " " +foutNewSol)
            f = open(foutNewSol)
            solution = f.readlines()
            f.close()
            # print appropriate message at standard output
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
                        print hex(curr-1)[-1], #last digit-1 in hex format is the number to right at current grid
                        f.write(str(hex(curr-1)[-1])+" ")
                        break
            print ""
            f.write("\n")

    #solve the game given in fgame text file, write the mapped sudoku solution to prob_#Mapped.txt, check for solution uniqueness
    def solve(self, fgame):
        fin = self.getOneGameRule(fgame)
        fout = fgame[:-4] + "sol.txt"
        os.system(minisat + " " + fin + " " + fout)
        f = open(fout)
        solution = f.readlines()
        f.close()
        if solution[0].startswith("UN"):
            print "Sorry. No Solution."
        else:
            assignment = solution[1].split()
            self.writeMapSolution(assignment, fout[:-4] + "Mapped.txt")
            self.checkUnique(assignment, fgame)
        return fout

#initialize the class
solver = SudukuSolver()
solver.getUniformRules() # generate the uniform rules for all games
inputs = glob.glob("SudokuPuzzles/prob_*.inp") # get all specified puzzles and solve
for inputFile in inputs:
    solver.solve(inputFile)
# solver.solve("SudokuPuzzles/prob_10.inp")

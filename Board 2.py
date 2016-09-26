#Author: Shuqi Liu.
# This class represents the board and imports and uses information from Piece.py class. The Board.py class should be called in the main or intialized first when working in the console
#The project represents the Back2Back puzzle. Allow basic piece placement, rotation and flip operation. Report error when illegal placement is attempted
#The board could be displayed and cleared.

from Piece import *

class Board():
    def __init__(self,initial = True,boardState=[]):
        self.iterateList = [(i,j) for i in range(5) for j in range(6)]
        self.iterateList.remove((4,5))
        self.iterateList.remove((4,4))
        self.iterateList.remove((3,5))
        self.deltah=0
        self.unused=['re','lb','pp','or','gr','ye','dg','db','p1','p2','bl']
        self.board=[[['emp','emp'] for j in range (6)] for i in range (5)]
        if not initial:
            #todo : using the action to recursively get the board or store the baord as the state of the nodes
            self.board=[]
            # print self.iterateList
            for i in range(5):
                line = []
                temp = boardState[i*36:(i+1)*36]
                for j in range(6):
                    curr = temp[j*6:(j+1)*6]
                    front = curr[0:3]
                    back = curr[3:]
                    line.append([front,back])
                    if front!='emp' and back!='emp':
                        try:
                            self.iterateList.remove((i,j))
                        except ValueError:
                            pass
                    try:
                        self.unused.remove(front[0:2])
                        self.unused.remove(back[0:2])
                    except ValueError:
                        pass
                self.board.append(line)
    def clear(self): #clear the board, get all pieces to initial unflipped states
        self.__init__()

    def getIterateList(self):
        return self.iterateList

    def getDeltah(self):
        return self.deltah

    def getunused(self):
        return self.unused

    def getCurrState(self):
        state = ""
        for row in self.board:
            for column in row:
                for entry in column:
                    state+=str(entry)
        return state

    def display(self):#show the current board
        print "\n2 Sides Board Occupancy Display :      --format-- (front,back), '+'placing from front side of the board, '-'placing from back of the board\n"
        for row in self.board:
            for entry in row:
                print "["+entry[0]+"," + entry[1]+"]    ",
            print ""

    #place a piece&check for errors, row,column are index of the top left corner of the piece placement row[0-4], column[0-5]
    #return True if placement successful, Flase otherwise
    def place(self,row,column,piece):
        if piece.getColor() not in self.unused:
            # print "Not availble: this piece",piece.getColor()," has been used."
            return False #when place a piece h change could not be -1 #False
        self.deltah = 0
        temp=[]
        currow=row
        for i in piece.getList():
            curr=[]
            currcol=column
            for depth in i:
               spot = self.place1grid(currow,currcol,depth,piece.getColor(),piece.getSide())
               if spot is None: #unsuccessful, ditch the entire operation, does not change the state of the board, report message
                   # print "Placement failed: piece",piece.getColor(),"Try Again.\n"
                   return False
               curr.append(spot)
               currcol+=1
            temp.append(curr)
            currow+=1

        #succeed, change the state of the board
        currow=row
        # print temp
        for i in temp:
            currcol=column
            for j in i:
                if (j[0]!='emp' and j[1]!='emp'):
                    # print "iterate List",j,currow,currcol,piece.getColor()
                    try:
                        self.iterateList.remove((currow,currcol))
                        print "removing location",currow,currcol,j
                    except ValueError:
                        pass
                self.board[currow][currcol] = j
                currcol+=1
            currow+=1
        self.unused.remove(piece.getColor()) #update the unused piece list
        # print "Placement succeeded: piece ",piece.getColor()#,"\n"
        return True


    # place 1 grid of a piece onto 1 spot on the board. If insert from front side, frontback = 0; from back side, frontback=1
    # return the spot recording the updated board state if successful, return None if unsuccessful
    def place1grid(self,row,column,depth,color,frontback):
        side = side= '+' if frontback==0 else '-'
        try:
            if row<0 or column<0: raise IndexError #catch the same way as indexoutofBounds
            spot = self.board[row][column]*1 # get the current occupancy state of grid on the board
            if depth==0: #always acceptable irrespect to board's occupancy state
                return spot
            if depth==1: #if the side we are inserting from is avaiable (='emp'), then accept the placement
                if spot[frontback]=='emp':
                    spot[frontback]=color+side
                    if spot[(frontback+1)%2] =='emp':self.deltah +=1 #emp to half minus 1
                    else: self.deltah +=2 #half to full, reduce by 1.5
                    if  (row==0 or row ==4):self.deltah +=0.5
                    if (column==0 or column==5): self.deltah+=0.5
                    return spot
            if depth==2: #both sides have to be empty to be an acceptable placement
                if spot[0]=="emp" and spot[1]=="emp": 
                    spot = [color+side,color+side]
                    self.deltah += 3 #empty to full, decrease by 3
                    if (row==0 or row ==4): self.deltah+=1 #side goes to 1 if, -4; corner goes to both if, -5
                    if (column==0 or column ==5): self.deltah+=1
                    return spot
            # print "Illegal Position: overlap not allowed at this position." #run through this step without return, unsuccessful attemp
            return None
        except IndexError:
            # print "Illegal Position: off the edge."
            return None

#initialize all the pegs in a 2D list, not all pegs have same sized list
def pieceInitialize():
    red=Piece([[2,2,1]],'re',0) #1X3 list
    lightblue=Piece([[2,1,2]],'lb',0)
    blue=Piece([[2,1,2],[0,0,1]],'bl',0) #2X3 list
    purple=Piece([[0,2,2],[1,1,0]],'pp',0)
    orange=Piece([[2,1,2],[1,0,0]],'or',0)
    green=Piece([[1,1,2],[2,0,0]],'gr',0)
    yellow=Piece([[2,2,1],[0,1,0]],'ye',0)
    darkgreen=Piece([[2,0],[1,2]],'dg',0) #2X2 list
    darkblue=Piece([[2,1],[2,0]],'db',0)
    pink1=Piece([[2,2],[1,0]],'p1',0)
    pink2=Piece([[2,2],[1,0]],'p2',0)
    print 'Pieces initialized'

    pieceDic={}
    pieceDic['re']=red
    pieceDic['lb']=lightblue
    pieceDic['bl']=blue
    pieceDic['pp']=purple
    pieceDic['or']=orange
    pieceDic['gr']=green
    pieceDic['ye']=yellow
    pieceDic['dg']=darkgreen
    pieceDic['db']=darkblue
    pieceDic['p1']=pink1
    pieceDic['p2']=pink2
    return red,lightblue,blue,purple,orange,green,yellow,darkgreen,darkblue,pink1,pink2,pieceDic

# print pieceDic['p2'].getColor()


def main():
    red,lightblue,blue,purple,orange,green,yellow,darkgreen,darkblue,pink1,pink2,pieceDic = pieceInitialize()
    board = Board()
    board.clear()
    board.display()
    lightblue.flip()
    lightblue.rotate()
    board.place(0,0,lightblue)
    darkgreen.flip()
    board.place(2,0,darkgreen)
    pink2.flip()
    for i in range(2):
        pink1.rotate()
    board.place(2,4,pink1)
    board.place(1,4,pink2)
    # for i in board.flipped:
    #     print i
    #"""
    # yellow.flip()
    # for i in range(2):
    #     yellow.rotate()
    # board.place(3,3,yellow) #overlap
    # board.place(-1,0,orange) #invalid index
    # board.place(4,4,purple) #off the edge
    # board.place(1,1,pink1) #used"""
    board.display()

    print board.getCurrState()
    newboard = Board(initial=False, boardState=board.getCurrState())
    print "\ndisplay new board!!!!"
    newboard.display()
    print newboard.unused
    print board.unused

#main()




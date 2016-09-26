import Queue;
import copy;
from Board import Board,pieceInitialize;
from Node import Node;
import time;
#todo : cite the resources of the package

# todo: current node - board placement, all unused ones try all remaining space,inefficient: for loop go through row and column
def getChildren(boardOriginal,parentPcost,parentHscore): #return a set of objects with type node
    children = []
    loop = boardOriginal.getIterateList()[:]
    for piece in boardOriginal.getunused():
        print "piece",piece
        piece=pieceDic[piece]
        board = copy.deepcopy(boardOriginal)
        for loc in loop:
            for rotation in range(4):
                for flip in range(2):
                    if board.place(loc[0],loc[1],piece):
                        children.append((Node(board,piece.getCost()+parentPcost,parentHscore-board.getDeltah(),piece)))
                        board = copy.deepcopy(boardOriginal)
                    piece.flip()
                piece.rotate()
    print "Found all the children",children
    return children

#subtract from parent score
def h2(board):
    score = 0
    for row in board.board[1:-1]:
        for index in [0,-1]:
            if row[index][0]=='emp' and row[index][1] =='emp':
                score+=3.5
            elif row[index][0]=='emp' or row[index][1] =='emp':
                score+=2.5
        for col in row[1:-1]:
            if col[0]=='emp' and col[1]=='emp':
                score += 3
            elif col[0]=='emp' or col[1]=='emp':
                score += 2
    side = board.board[0]+board.board[-1]
    for entry in side:
        if entry[0]=='emp' and entry[1]=='emp':
            score+=3.5
        elif entry[0]=='emp' or entry[1] =='emp':
            score+=2.5

    side = [board.board[0][0],board.board[-1][-1],board.board[-1][0],board.board[0][-1]]
    for entry in side:
        if entry[0] == 'emp' or entry[1] =='emp':
            score+=1
    return score

# todo: score the board once, go through everything at the start state;
# todo: later when score update the previous step score

def h(board):
    score=0
    for row in board.board:
        for col in row:
            if col[0]=='emp' and col[1]=='emp':
                score += 2
            elif col[0]=='emp' or col[1]=='emp':
                score += 1.5
    return score

 #only the string representing state is stored in the explored  set
def Astar(start,startboard):
    pqueue = Queue.PriorityQueue()
    pqueue.put((start.getHscore()+start.getPcost(),start)) #what is the h(start)
    explored = set()
    counter=-1e-10
    while not pqueue.empty():
        curr = pqueue.get_nowait()[1]
        print "\npriority queue",curr.getColor(),"size",pqueue.qsize()
        print curr
        currboard = curr.getStateBoard()
        if not currboard.getunused():#if unused is empty, only successful placement will remove unusued
            print "\nDone\n","Final Result:"
            currboard.display()
            return curr.getPcost(),explored.__len__()
        else:
            explored.add(curr.getState())
            # currboard.display()
            for child in getChildren(currboard,curr.getPcost(),curr.getHscore()):
                print "child current ready to be enqueued",child.getColor()
                if child.getState() not in explored:
                    child.setParent(curr)
                    pqueue.put((child.getHscore()+child.getPcost()+counter,child))
                    counter-=1e-12
                    # print "child Hscore", child.getHscore()
    print "Failed Attempt"
    return None


def level1(board):
    board.place(0,0,pink1)
    red.rotate()
    red.flip()
    board.place(0,2,red)
    for i in range(2):
        darkgreen.rotate()
    darkgreen.flip()
    board.place(1,0,darkgreen)
    green.rotate()
    board.place(2,1,green)
    lightblue.flip()
    lightblue.rotate()
    board.place(0,3,lightblue)
    board.place(0,3,purple)
    orange.rotate()
    orange.rotate()
    board.place(3,3,orange)
    yellow.rotate()
    yellow.flip()
    board.place(2,4,yellow)
    cost = 0
    for i in board.onBoard:
        cost+= i.getCost()
    return board,cost

def level3(board): #1,3,4; k=9
    red.flip()
    red.rotate()
    board.place(0,0,red)
    orange.rotate()
    board.place(0,0,orange)
    purple.flip()
    purple.rotate()
    purple.rotate()
    board.place(1,1,purple)
    yellow.flip()
    for i in "abc":
        darkblue.rotate()
        yellow.rotate()
    board.place(0,4,darkblue)
    board.place(2,4,yellow)
    board.place(3,2,pink1)
    blue.rotate()
    board.place(2,4,blue)
    board.place(0,2,darkgreen)
    green.flip()
    green.rotate()
    green.rotate()
    board.place(3,1,green)
    cost = 0
    for i in board.onBoard:
        cost+= i.getCost()
    return board,cost

def level4(board):
    for i in "abc":
        pink1.rotate()
        pink2.rotate()
        darkblue.rotate()
        red.rotate()
    board.place(0,0,pink1)
    board.place(0,4,pink2)
    board.place(0,2,darkblue)
    board.place(2,5,red)
    blue.flip()
    board.place(0,1,blue)
    lightblue.flip()
    lightblue.rotate()
    board.place(2,0,lightblue)
    darkgreen.flip()
    darkgreen.rotate()
    darkgreen.rotate()
    board.place(3,1,darkgreen)
    orange.rotate()
    orange.rotate()
    board.place(3,2,orange)
    green.flip()
    green.rotate()
    board.place(0,4,green)
    cost = 0
    for i in board.onBoard:
        cost+= i.getCost()
    return board,cost

def level2(board): #2,5,10; k=8
    pass
def level6(board):#6,7,9; k=7
    pass
def level8(board):#8,17,18; k=6
    pass
def level11(board): #11,13,14; k=5
    pass

def level13(board):#14,11
    board.place(1,2,pink1)
    pink2.flip()
    pink2.rotate()
    pink2.rotate()
    pink2.rotate()
    board.place(1,4,pink2)
    lightblue.flip()
    lightblue.rotate()
    board.place(0,0,lightblue)
    darkgreen.flip()
    board.place(2,0,darkgreen)
    yellow.flip()
    yellow.rotate()
    yellow.rotate()
    board.place(3,3,yellow)
    cost = 0
    for i in board.onBoard:
        cost+= i.getCost()
    return board,cost

def level25(board): #25,26,27; 4 on board
    blue.flip()
    blue.rotate()
    blue.showpiece()
    board.place(0,0,blue)
    green.rotate()
    board.place(1,2,green)
    purple.rotate()
    purple.flip()
    board.place(1,2,purple)
    board.place(3,1,darkgreen)
    
    board.display()
    assert(1==2)

    cost = 0
    for i in board.onBoard:
        cost+= i.getCost()
    return board,cost

def level26(board):#25,27
    yellow.rotate()
    yellow.rotate()
    yellow.rotate()
    board.place(1,0,yellow)
    purple.rotate()
    purple.rotate()
    purple.rotate()
    board.place(0,2,purple)
    red.flip()
    board.place(2,3,red)
    blue.flip()
    board.place(3,1,blue)
    cost = 0
    for i in board.onBoard:
        cost+= i.getCost()
    return board,cost

def level38(board): #38,39,40; 3 on board
    lightblue.flip()
    board.place(0,3,lightblue)
    blue.flip()
    for i in range(3):
        blue.rotate()
    board.place(2,0,blue)
    red.flip()
    board.place(4,2,red)
    cost = 0
    for i in board.onBoard:
        cost+= i.getCost()
    return board,cost

def level39(board):
    blue.flip()
    board.place(0,2,blue)
    pink1.flip()
    board.place(3,0,pink1)
    pink2.flip()
    for i in range(3):
        pink2.rotate()
    board.place(3,4,pink2)
    cost = 0
    for i in board.onBoard:
        cost+= i.getCost()
    return board,cost

def level40(board):
    for i in "abc":
        blue.rotate()
    board.place(0,2,blue)
    pink1.flip()
    pink1.rotate()
    pink1.rotate()
    board.place(0,3,pink1)
    green.flip()
    green.rotate()
    board.place(2,2,green)
    cost = 0
    for i in board.onBoard:
        cost+= i.getCost()
    return board,cost

def level49(board): #49,50,52; 2 on board
    lightblue.flip()
    lightblue.rotate()
    board.place(0,3,lightblue)
    orange.rotate()
    board.place(0,0,orange)
    cost = 0
    for i in board.onBoard:
        cost+= i.getCost()
    return board,cost



def level58(board): #58,59,60; 1 on board
    pass
def level59(board):
    pink1.rotate()
    board.place(1,3,pink1)
    cost = 0
    for i in board.onBoard:
        cost+= i.getCost()
    return board,cost

def level34(board):
    darkblue.flip()
    darkblue.rotate()
    darkblue.rotate()
    board.place(0,1,darkblue)
    blue.flip()
    board.place(0,3,blue)
    lightblue.rotate()
    board.place(2,3,lightblue)
    orange.rotate()
    orange.rotate()
    orange.showpiece()
    board.place(0,2,orange)
    cost = 0
    for i in board.onBoard:
        cost+= i.getCost()
    return board,cost

def level44(board):
    board = Board()
    board.clear()
    pink1.flip()
    pink1.rotate()
    pink1.rotate()
    pink1.rotate()
    board.place(0,0,pink1)
    board.place(0,1,green)
    board.place(2,3,darkgreen)
    cost = 0
    for i in board.onBoard:
        cost+= i.getCost()
    return board,cost

def level48(board):
    board = Board()
    board.clear()
    pink1.rotate()
    pink1.rotate()
    board.place(3,3,pink1)
    darkgreen.flip()
    darkgreen.rotate()
    board.place(3,1,darkgreen)
    yellow.flip()
    yellow.rotate()
    yellow.showpiece()
    board.place(2,4,yellow)
    cost = 0
    for i in board.onBoard:
        cost+= i.getCost()
    return board,cost



def main():
    board = Board()
    board.clear()
    # for level in [38]:#,2,5,10,6,7,9,8,17,18,11,13,14,25,26,27,38,39,40,40,50,52,58,59,60]:
    level = 25
    start_time = time.time()
    board.clear()
    board,start_cost=eval('level'+str(level)+'(board)') #1,3,4;-13;-26;-38,39,;-49; --8,34,44-- DN run: 59,39,26
    # print board.getunused()
    print "start:"
    board.display()
    start = Node(board,start_cost,h(board),None) #action =[]
    print "start state string:",start.getState()
    print start.getPcost(),start.getHscore()
    pathCost,exploredSize = Astar(start,board)
    assert(pathCost==60),"Wrong Solution"
    print "Path Cost",pathCost,"Explored Set Size",exploredSize
    runtime = time.time()-start_time
    print "Running time:",runtime
    f= open("experimentResult.txt",'a')
    f.write("level"+str(level)+"    "+str(exploredSize)+"    "+str(runtime)+"    "+str(pathCost)+"\n")
    f.close()

red,lightblue,blue,purple,orange,green,yellow,darkgreen,darkblue,pink1,pink2,pieceDic = pieceInitialize()
main()


import Queue;
import copy;
from Board import Board,pieceInitialize;
from Node import Node;
import time;
#todo : cite the resources of the package

start_time = time.time()

# todo: current node - board placement, all unused ones try all remaining space,inefficient: for loop go through row and column
def getChildren(boardOriginal,parentPcost,parentHscore): #return a set of objects with type node
    children = []
    # print "original parameter"
    # boardOriginal.display()
    loop = boardOriginal.getIterateList()[:]
    for piece in boardOriginal.getunused():
        print "piece",piece
        piece=pieceDic[piece]
        board = copy.deepcopy(boardOriginal)
        # print "copied board"
        # board.display()
        # for loc in [(j,i) for j in range(5) for i in range(6)]:
        # print "Don't revisit here"
        for loc in loop:
            for rotation in range(4):
                for flip in range(2):
                    if board.place(loc[0],loc[1],piece):
                        children.append((Node(board,piece.getCost()+parentPcost,parentHscore-board.getDeltah(),piece)))
                        print "children update:",children
                        board = copy.deepcopy(boardOriginal)
                    piece.flip()
                piece.rotate()
    print "leaving getChildren for loop"
    return children

#subtract from parent score
def h2(board):
    score = 0
    for row in board.board[1:-1]:
        # print "row0,-1",row[0],row[-1]
        for index in [0,-1]:
            if row[index][0]=='emp' and row[index][1] =='emp':
                score+=3.5
            elif row[index][0]=='emp' or row[index][1] =='emp':
                score+=2.5
        for col in row[1:-1]:
            # print col
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
        # currboard.display()
        if not currboard.getunused():#if unused is empty, only successful placement will remove unusued
            print "\nDone\n","Final Result:"
            currboard.display()
            print "Explored Set Size", explored.__len__()
            # while True:
            #     print "pop from set"
            #     Board(False,explored.pop()).display()
            return curr.getPcost()
        else:
            # print "---------here!!!---------"
            explored.add(curr.getState())
            currboard.display()
            for child in getChildren(currboard,curr.getPcost(),curr.getHscore()):
                print "child current ready to be enqueued",child.getColor()
                if child.getState() not in explored:
                    child.setParent(curr)
                    pqueue.put((child.getHscore()+child.getPcost()+counter,child))
                    counter-=1e-12
                    # print "child Hscore", child.getHscore()
    print "Failed Attempt"
    return False
#when call getChildren, turn the string representation into a board, and operate the place method properly

def level1(board):
    onBoard=[]
    board.place(0,0,pink1)
    onBoard.append(pink1)
    red.rotate()
    red.flip()
    board.place(0,2,red)
    onBoard.append(red)
    for i in range(2):
        darkgreen.rotate()
    darkgreen.flip()
    board.place(1,0,darkgreen)
    onBoard.append(darkgreen)
    green.rotate()
    board.place(2,1,green)
    onBoard.append(green)
    lightblue.flip()
    lightblue.rotate()
    board.place(0,3,lightblue)
    onBoard.append(lightblue)
    board.place(0,3,purple)
    onBoard.append(purple)
    orange.rotate()
    orange.rotate()
    board.place(3,3,orange)
    onBoard.append(orange)
    yellow.rotate()
    yellow.flip()
    board.place(2,4,yellow)
    onBoard.append(yellow)
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
def level25(board): #25,26,27; 4 on board
    pass
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

def level49(board): #49,50,52; 2 on board
    pass
def level58(board): #58,59,60; 1 on board
    pass
def level59(board):
    onBoard=[]
    pink1.rotate()
    board.place(1,3,pink1)
    onBoard.append(pink1)
    cost = 0
    for i in onBoard:
        cost+= i.getCost()
    return board,cost

def level48(board):
    onBoard=[]
    board = Board()
    board.clear()
    pink1.rotate()
    pink1.rotate()
    board.place(3,3,pink1)
    onBoard.append(pink1)
    darkgreen.flip()
    darkgreen.rotate()
    board.place(3,1,darkgreen)
    onBoard.append(darkgreen)
    yellow.flip()
    yellow.rotate()
    yellow.showpiece()
    board.place(2,4,yellow)
    onBoard.append(yellow)
    cost = 0
    for i in onBoard:
        cost+= i.getCost()
    return board,cost

def level44(board):
    onBoard=[]
    board = Board()
    board.clear()
    pink1.flip()
    pink1.rotate()
    pink1.rotate()
    pink1.rotate()
    board.place(0,0,pink1)
    onBoard.append(pink1)
    board.place(0,1,green)
    onBoard.append(green)
    board.place(2,3,darkgreen)
    onBoard.append(darkgreen)
    cost = 0
    for i in onBoard:
        cost+= i.getCost()
    return board,cost

def level34(board):
    onBoard=[]
    darkblue.flip()
    darkblue.rotate()
    darkblue.rotate()
    board.place(0,1,darkblue)
    onBoard.append(darkblue)
    blue.flip()
    board.place(0,3,blue)
    onBoard.append(blue)
    lightblue.rotate()
    board.place(2,3,lightblue)
    onBoard.append(lightblue)
    orange.rotate()
    orange.rotate()
    orange.showpiece()
    board.place(0,2,orange)
    onBoard.append(orange)
    cost = 0
    for i in onBoard:
        cost+= i.getCost()
    return board,cost

def level13(board):#14,11
    onBoard=[]
    board.place(1,2,pink1)
    onBoard.append(pink1)
    pink2.flip()
    pink2.rotate()
    pink2.rotate()
    pink2.rotate()
    board.place(1,4,pink2)
    onBoard.append(pink2)
    board.display()
    lightblue.flip()
    lightblue.rotate()
    board.place(0,0,lightblue)
    onBoard.append(lightblue)
    darkgreen.flip()
    board.place(2,0,darkgreen)
    onBoard.append(darkgreen)
    yellow.flip()
    yellow.rotate()
    yellow.rotate()
    board.place(3,3,yellow)
    onBoard.append(yellow)
    cost = 0
    for i in onBoard:
        cost+= i.getCost()
    return board,cost

def level26(board):#25,27
    onBoard=[]
    yellow.rotate()
    yellow.rotate()
    yellow.rotate()
    board.place(1,0,yellow)
    onBoard.append(yellow)
    purple.rotate()
    purple.rotate()
    purple.rotate()
    board.place(0,2,purple)
    onBoard.append(purple)
    red.flip()
    board.place(2,3,red)
    onBoard.append(red)
    blue.flip()
    board.place(3,1,blue)
    onBoard.append(blue)
    cost = 0
    for i in onBoard:
        cost+= i.getCost()
    return board,cost


def level39(board):
    onBoard=[]
    blue.flip()
    board.place(0,2,blue)
    onBoard.append(board)
    pink1.flip()
    board.place(3,0,pink1)
    pink2.flip()
    for i in range(3):
        pink2.rotate()
    board.place(3,4,pink2)
    onBoard = [pink1,pink2,blue]
    cost = 0
    for i in onBoard:
        cost+= i.getCost()
    return board,cost



def level49(board):
    pass

def main():
    board = Board()
    board.clear()
    board,start_cost=level4(board) #34,44,1,48,13,26,39,49, DN run: 59,39,26
    print board.getunused()
    print "start:"
    board.display()
    start = Node(board,start_cost,h(board),None) #action =[]
    print "start state string:",start.getState()
    print start.getPcost(),start.getHscore()
    pathCost = Astar(start,board)
    assert pathCost ==60
    print "Running time:",time.time()-start_time

red,lightblue,blue,purple,orange,green,yellow,darkgreen,darkblue,pink1,pink2,pieceDic = pieceInitialize()
main()


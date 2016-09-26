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
    pass
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
    onBoard=[]
    lightblue.flip()
    board.place(0,3,lightblue)
    blue.flip()
    for i in range(3):
        blue.rotate()
    board.place(0,2,blue)
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

def level44(board):
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
    board,start_cost=level1(board) #34,44,1,48,13,26,39,49, DN run: 59,39,26
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


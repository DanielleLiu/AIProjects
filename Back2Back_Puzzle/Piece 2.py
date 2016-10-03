#Author: Shuqi Liu
#This class provides basic show, rotate, and flip functions, constuctors and getters for the pieces
#Should be imported into Board.py and work in Board.py

class Piece():
    def __init__(self,listvalue,color,side):
        self.color=color
        self.side=side #0 front, 1 flipped
        self.list=[]
        self.list = [row for row in listvalue]

    def rotate(self):#rotate Clockwise
        temp=[]
        columns=len(self.list[0])
        for i in range(columns):
            curr=[row[i] for row in self.list]
            curr.reverse()
            temp.append(curr)
        self.list=temp

    def showpiece(self):
        side= 'front' if self.side==0 else 'back'
        print self.color,side
        for i in self.list:
            print i
        print " "

    def flip(self): #vertical flip/rotate 180 degrees
        for i in self.list:
            i.reverse()
        self.side=(self.side+1)%2
        return self

    def getColor(self):
        return self.color

    def getSide(self):
        return self.side

    def getList(self):
        return self.list

    def getSize(self): #return Number of rows,Number of columns
        return len(self.list),len(self.list[0])

    def getCost(self):
        cost=0
        for i in self.list:
            cost+=sum(i)
        return cost


"""
def main():
    # red=Piece([[2,2,1]],'r',0) #uniform the size to 3X3, when rotate later on?
    # lightblue=Piece([[2,1,2]],'lb',0)
    # blue=Piece([[2,1,2],[0,0,1]],'b',0)
    # purple=Piece([[0,2,2],[1,1,0]],'p',0)
    # orange=Piece([[2,1,2],[1,0,0]],'o',0)
    # green=Piece([[1,1,2],[2,0,0]],'g',0)
    # yellow=Piece([[2,2,1],[0,1,0]],'y',0)
    # darkgreen=Piece([[2,0],[1,2]],'dg',0)
    # darkblue=Piece([[1,0],[2,2]],'db',0)
    # pink1=Piece([[2,2],[1,0]],'pk1',0)
    # pink2=Piece([[2,2],[1,0]],'pk2',0)
    # print 'Pieces initialized'

    lightblue.showpiece()
    pink1.showpiece()
    orange.showpiece()
    orange.flip()
    orange.showpiece()
    print pink1.getList()
    pink1.showpiece()
    pink1.flip()
    pink1.showpiece()
    pink1.rotate()
    pink1.showpiece()
    pink1.rotate()
    pink1.showpiece()
    pink1.rotate()
    pink1.showpiece()
    pink1.rotate()
    pink1.showpiece()
    pink1.flip()
    pink1.showpiece()
    pink1.flip()
    pink1.showpiece()
    pink1.flip()
    pink1.showpiece()
    # print pink2.getColor()
    # print pink2.getSide()
    # print pink1.getSide()

#main()

"""


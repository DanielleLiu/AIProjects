class Node():
    def __init__(self,state,pcost,hscore,piececolor,action=[],parent = None): #prioritize based on gn+hn
        self.state=state #a string representation of current board state
        self.parent=parent # reference to the parent
        self.action=action #a string or list of strings indicating the actions
        self.pcost=pcost #an integer represents the path cost
        self.hscore = hscore
        self.piececolor = piececolor

    def getHscore(self):
        return self.hscore

    def getParent(self): # return a reference
        return self.parent

    def getColor(self):
        return self.piececolor

    def getAction(self): # return a string or a list of strings
        return self.action

    def getState(self): #return a string
        return self.state

    def getPcost(self): # return an integer
        return self.pcost

    def setPcost(self,newPcost):
        self.pcost=newPcost

    def setParent(self,parentNode):
        self.parent=parentNode
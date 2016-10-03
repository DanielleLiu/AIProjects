c1= None
c2 = None

if (c1 or c2):
    print "True"
else:
    print "ohhhh"

c1 = True

if (c1 or c2):
    print "True"
else:
    print "ohhhh"

model =[1,2,3]
def testReturn(model):
    if model[0] == -1:
        print model
        return True
    if model[0] ==10:
        print model
        return False
    newModel1 = model
    new2 = model
    newModel1[0]=-1
    new2[0]=10
    print "cur new",newModel1,new2
    return testReturn(newModel1) or testReturn(new2)

print "test", testReturn(model)
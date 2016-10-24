import itertools
import numpy as np

# a = ["{:03x}".format(i,'X') for i in xrange(0x0,0x10)]
# b =  itertools.combinations(a,2)
# lent = 0
# for i in b:
#     print i
#     lent+=1
# print len (a),a
# print lent
# and
# not x001 or not x002
# not x001 or not x003




# variableString = ["{:03x}".format(i, 'X') for i in xrange(0x000, 0x1000)]
# variableString = [i for i in range(int(0x000)+1, int(0x1000)+1)]
# allvars = np.array(variableString)
# allvars = allvars.reshape(16, 16, 16)
# # print allvars[0,:,:] #all grid for first row
# temp = allvars[4:8,0:4,0]#.tolist() #all grid for first row
# # list = []
# # for i in temp:
# #     list+=i
# print temp
# list = np.hstack(temp)
# print list


# for i in range(16): rows unique
#     rows = self.allvars[:,:,i]
#     for row in row:
#         self.exactlyOne(row)
# for i in range(16): #exactly one pe rgrid
#     row = self.allvars[i,:,:] #all grid for first row
#     for grid in row:
#         count+=self.exactlyOne(grid)
# print count


b = hex(10) #Oxa in string

for i in range(4):
    for j in range(4):
        if j==1:
            break
        print j
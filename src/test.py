import numpy
import sys
import read_ini as RE
##
##a = {'x1':1, 'x2':2}
##if 'x1' in a:
##    print 'zai'
##
##F_open=open("../data/user_list.txt", "r")
##i = 0
##for Line in F_open:
##    print Line.split()
##    i =  i + 1
##    if(i > 10):
##        break

def user_list(File_Name):
    F_open=open(File_Name, "r")
    User_Name={}
    User_Id={}
    User_Num = 0
    for Line in F_open:
        print Line.split()
        [U_Id, U_Name] = Line.split()
        U_Id = int(U_Id)
        User_Name[U_Name] = U_Id
        User_Id[U_Id] = U_Name
        User_Num = User_Num + 1
    return [User_Name, User_Id, User_Num]
##user_list("../data/user_list.txt")


a = numpy.matrix([4, 2, 3, 1, 7])
a = a * -1
print a.argsort()
print a.shape
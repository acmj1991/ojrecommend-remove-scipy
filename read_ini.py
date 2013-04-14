# -*- coding: utf-8 -*- #
import numpy
import sys


def read_conf(conf_file):
    re_conf = {}
    f_op = open(conf_file, "r")
    for Line in f_op:
        if(Line[0] == '#'):
            continue
        [name, val] = Line.split("=")
        re_conf[name] = val.split("\n")[0]
    return re_conf

def get_pro_num(file_name):
    f_open = open(file_name, "r")
    count = int(0)
    for Line in f_open:
        [ID, Score] = Line.split()
        if(count < int(ID)):
            count = int(ID)
    return count

#获取name以及对应的id
def user_list(File_Name):
    F_open=open(File_Name, "r")
    User_Name={}
    User_Id={}
    User_Num = 0
    for Line in F_open:
        [U_Id, U_Name] = Line.split()
        U_Id = int(U_Id)
        User_Name[U_Name] = U_Id
        User_Id[U_Id] = U_Name
        User_Num = User_Num + 1
    return [User_Name, User_Id, User_Num]

#获取用户ac题目矩阵
def pro_user_matrix(File_Name, User_Name, Pro_Sum, N):
    F_open=open(File_Name, "r")
    User_AC_Pro = [[0 for i in range(len(User_Name) + 1)] for j in range(Pro_Sum + 2)]
    User_AC_Sum = [0 for i in range(len(User_Name) + 1)]
    Pro_AC_Sum = [0 for i in range(Pro_Sum + 2)]
    for Line in F_open:
        [Pro_Id, U_Name, Answer] = Line.split()
        if U_Name in User_Name:
            U_Id = (int)(User_Name[U_Name])
            Pro_Id = int(Pro_Id)
            if User_AC_Pro[Pro_Id][U_Id] == 0:
                if User_AC_Sum[U_Id] <= N:
                    User_AC_Pro[Pro_Id][U_Id] = 1
                User_AC_Sum[U_Id] += 1
                Pro_AC_Sum[Pro_Id] += 1
    User_AC_Pro_Matrix = numpy.matrix(User_AC_Pro, float)
    return [User_AC_Pro_Matrix, User_AC_Sum, Pro_AC_Sum]


#根据难度获取题目与题目的相似度
def get_score_sim(File_Name, Pro_Num, Weight):
    fp = open(File_Name, "r")
    score_list = [0 for i in range(Pro_Num + 2)]
    score_matrix = [[0 for i in range(Pro_Num + 2)] for j in range(Pro_Num + 2)]
    #print score_matrix
    for Line in fp:
        [ID, Score] = Line.split()
        IDD = int(ID)
        score_list[IDD] = int(Score)
    for i in range(Pro_Num):
        for j in range(Pro_Num):
            if i == 0 or j == 0:
                continue
            row = int(i)
            col = int(j)
            score_matrix[row][col] = int(score_list[col] - score_list[row] + Weight)
    return score_matrix

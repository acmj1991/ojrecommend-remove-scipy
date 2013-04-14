# -*- coding: utf-8 -*- #
import numpy
import sys
import read_ini as RE
#import scipy.sparse as SC
#from scipy import *


#根据用户ac记录获取题目和题目的相似度
def pro_pro_simily(User_AC_Pro_Matrix, User_AC_Sum, Pro_Num):
    User_Model = numpy.multiply(User_AC_Pro_Matrix, User_AC_Pro_Matrix)
    User_User_Model = User_Model.sum(1)
    User_User_Model = User_User_Model * User_User_Model.T
    #print User_User_Model
    numpy.power(User_User_Model, 0.5, User_User_Model)

    User_AC_Sum_Matrix = numpy.matrix(User_AC_Sum, float)
    Model = numpy.matrix([1 for i in range(Pro_Num + 2)])
    User_AC_Sum_Matrix = Model.T * User_AC_Sum_Matrix

    #难度加权
    User_AC_Pro_Matrix = numpy.divide(User_AC_Pro_Matrix, numpy.log2(User_AC_Sum_Matrix + 2))


    #User_AC_Pro_Matrix = SC.csc_matrix(User_AC_Pro_Matrix)
    User_AC_Pro_Matrix = (User_AC_Pro_Matrix * User_AC_Pro_Matrix.T)#.todense()
    #print User_AC_Pro_Matrix

    Pro_Pro_Dot = numpy.divide(User_AC_Pro_Matrix, (User_User_Model + 1))

    for i in range(Pro_Num):
        Pro_Pro_Dot[i, i] = 0

    return Pro_Pro_Dot


#保留相似度最大的前N个
def get_front_N(Pro_Pro_Simily, N):
    size = Pro_Pro_Simily.shape[1]
    Pro_Pro_Simily[Pro_Pro_Simily<Pro_Pro_Simily[range(0,size),Pro_Pro_Simily.argsort()[:, size - N -1].T].T.repeat(size, 1)]=0
    return Pro_Pro_Simily

#输出User_Id的结果
def show_ans(ans_file, User_Id, User_Rcomend_Pro_Mat, Pro_Num, Ans_num, User_Num):
    fp = open(ans_file, "w")
    for u_id in range(0,User_Num):
        fp.write(str(u_id))
        for i in range(1, Ans_num):
            id = (int(i))
            fp.write(" " + str(User_Rcomend_Pro_Mat[u_id].argsort()[0, id]))
        fp.write("\n");
    fp.close()
    #print User_Rcomend_Pro_Mat[ID].argsort()


#---------------------------main()-------------------------------------

#从配置文件读取配置数据
file_conf = RE.read_conf("../conf/recommend.ini")

#文件路径
user_file = "../data/user_list.txt"#file_conf["user_list_file"]
score_file = "../data/score.txt"#file_conf["score_file"]
rev_file = "../data/rev.txt"#file_conf["rev_file"]
ans_file = "../data/ans.txt"#file_conf["ans_file"]

#取相似度最大题目的个数
Front_sim_N = int(file_conf["Front_sim_N"])

#推荐所使用最后ac题目的个数
Front_AC_N = int(file_conf["Front_AC_N"])

#提供推荐结果数
Ans_num = int(file_conf["Ans_num"])

#获取name与id的字典
[User_Name, User_Id, User_Num] = RE.user_list(user_file)

#题目个数
Pro_Num = RE.get_pro_num(score_file)


#求出用户已ac题目矩阵
[User_AC_Pro_Matrix, User_AC_Sum, Pro_AC_Sum] = RE.pro_user_matrix(rev_file, User_Name, Pro_Num, Pro_Num+1000)

#求出基于难度的矩阵
score_matrix = RE.get_score_sim(score_file, Pro_Num, 10)

#求出基于物品相似度矩阵
Pro_Pro_Simily = pro_pro_simily(User_AC_Pro_Matrix, User_AC_Sum, Pro_Num) #* 100 + score_matrix
#获取相似度最大部分题目
Pro_Pro_Simily = get_front_N(Pro_Pro_Simily, Front_sim_N)

#获取最后ac的Front_AC_N道题目
[User_AC_Pro_Matrix_Front, User_AC_Sum_Front, Pro_AC_Sum_Front] = RE.pro_user_matrix(rev_file, User_Name, Pro_Num, Front_AC_N)
User_Rcomend_Pro_Mat = Pro_Pro_Simily * User_AC_Pro_Matrix_Front

#print User_Rcomend_Pro_Mat
#去掉已经ac的题目
User_Rcomend_Pro_Mat[User_AC_Pro_Matrix > 0] = 0
User_Rcomend_Pro_Mat = User_Rcomend_Pro_Mat.T * -1

#展示结果
show_ans(ans_file, User_Id, User_Rcomend_Pro_Mat, Pro_Num, Ans_num, User_Num)





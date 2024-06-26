import scipy.sparse as sp
import numpy as np
import pandas as pd


def load_rating_file_as_list():
    ratingList = []
    with open('ml-100k/ml-100k.test.rating', "r") as f:
        line = f.readline()
        while line != None and line != "":
            arr = line.split("\t")
            user, item = int(arr[0]), int(arr[1])
            ratingList.append([user, item])
            line = f.readline()
    return ratingList


def load_negative_file():
    negativeList = []
    with open('ml-100k/ml-100k.test.negative', "r") as f:
        line = f.readline()
        while line != None and line != "":
            arr = line.split("\t")
            negatives = []
            for x in arr[1:]:
                negatives.append(int(x))
            negativeList.append(negatives)
            line = f.readline()
    return negativeList


def load_rating_train_as_matrix():
        # Get number of users and items
    num_users, num_items = 0, 0
    with open("ml-100k/u.info", "r") as f:
        line = f.readline()
        while line != None and line != "":
            arr = line.split(" ")
            if(arr[1].replace("\n", "") == 'users'):
                num_users = int(arr[0])
            if (arr[1].replace("\n", "") == 'items'):
                num_items = int(arr[0])
            line = f.readline()

    # Construct matrix
    mat = sp.dok_matrix((num_users + 1, num_items + 1), dtype=np.float32)
    with open('ml-100k/ml-100k.train.rating', "r") as f:
        line = f.readline()
        while line != None and line != "":
            arr = line.split("\t")
            user, item, rating = int(arr[0]), int(arr[1]), float(arr[2])
            if (rating > 0):
                mat[user, item] = 1.0
            line = f.readline()
    return mat


def load_itemGenres_as_matrix():
    num_items, num_type, dict = 0, 0, {}
    with open("ml-100k/u.info") as f:
        line = f.readline().strip('\n')
        while line != None and line != "":
            arr = line.split(" ")
            if (arr[1] == 'items'):
                num_items = int(arr[0])
            line = f.readline().strip('\n')

    with open("ml-100k/u.genre", "r") as f:
        line = f.readline().strip('\n')
        while line != None and line != "":
            arr = line.split("|")
            dict[arr[0]] = num_type
            num_type = num_type + 1
            line = f.readline().strip('\n')

    # Construct matrix
    mat = sp.dok_matrix((num_items + 1, num_type), dtype=np.float32)
    with open("ml-100k/movies100k.dat",encoding="utf-8-sig") as f:
        line = f.readline().strip('\r\n')
        #i=0
        while line != None and line != "":
            arr = line.split("::")
            if len(arr)>=3:
                types = arr[2].split("|")
                for ts in types:
                    if (ts in dict.keys()):
                        mat[int(arr[0]), dict[ts]] = 1
            #i = i + 1
            line = f.readline().strip('\r\n')
            itemGenres_mat = mat.toarray()
        #else:
            #print(i)

    return num_items, itemGenres_mat


def load_user_attributes():
    usersAttributes = []
    num_users = 0
    dictGender = {}
    genderTypes = 0
    dictAge = {}
    ageTypes = 0
    dictOccupation = {}
    ocTypes = 0

    with open('ml-100k/users.dat', "r") as f:
        line = f.readline().strip('\n')
        while line != None and line != "":
            arr = line.split('::')
            l = []
            for x in arr[0:4]:
                l.append(x)
            usersAttributes.append(l)
            line = f.readline().strip('\n')
    usersAttrMat = np.array(usersAttributes)

    num_users = len(usersAttrMat)

    # one-hot encoder

    # age types

    genders = set(usersAttrMat[:, 1])
    for gender in genders:
        dictGender[gender] = genderTypes
        genderTypes += 1

    # age types
    ages = set(usersAttrMat[:, 2])
    for age in ages:
        dictAge[age] = ageTypes
        ageTypes += 1

    # occupation types
    ocs = set(usersAttrMat[:, 3])
    for oc in ocs:
        dictOccupation[oc] = ocTypes
        ocTypes += 1

    # Gender,Age,Occupation
    gendermat = sp.dok_matrix((num_users + 1, genderTypes), dtype=np.float32)
    agemat = sp.dok_matrix((num_users + 1, ageTypes), dtype=np.float32)
    occupationmat = sp.dok_matrix((num_users + 1, ocTypes), dtype=np.float32)

    with open("ml-100k/users.dat") as f:
        line = f.readline().strip('\n')
        while line != None and line != "":
            arr = line.split("::")
            userid = int(arr[0])
            usergender = arr[1]
            userage = arr[2]
            useroc = arr[3]
            # gender encoder
            if usergender in dictGender.keys():
                gendermat[userid, dictGender[usergender]] = 1.0
            # age encoder
            if userage in dictAge.keys():
                agemat[userid, dictAge[userage]] = 1.0
            # occupation encoder
            if useroc in dictOccupation.keys():
                occupationmat[userid, dictOccupation[useroc]] = 1.0

            line = f.readline().strip('\n')
        user_gender_mat = gendermat.toarray()
        user_age_mat = agemat.toarray()
        user_oc_mat = occupationmat.toarray()

    # concatenate Gender[0-1], Age[], Occupation
    #onehotUsers = np.hstack((user_gender_mat, user_age_mat, user_oc_mat))
    return num_users, user_gender_mat, user_age_mat, user_oc_mat


def load_user_vectors():
    userNeighbors = open('neighbors/interNeighbors_20.txt').readlines()
    #userNeighbors = open('neighbors/hammingNeighbors_20.txt').readlines()

    userVecmat = [[0] * 20]
    for u in userNeighbors:
        u = u.strip('\n')
        nbs = u.split('\t')
        #nbs = u.split(' ')
        userVecmat.append(nbs[0:20])
    mat = np.array(userVecmat)
    return mat

#ratinglist=load_rating_file_as_list()
negativelist=load_negative_file()
rating=load_rating_train_as_matrix()
_,itemgene=load_itemGenres_as_matrix()
_,user_gender_mat, user_age_mat, user_oc_mat=load_user_attributes()
#print(ratinglist)
#print(negativelist)
#print(rating.shape)
print(itemgene.shape)
print(user_gender_mat.shape)
print(user_age_mat.shape)
print(user_oc_mat.shape)
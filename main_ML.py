import pandas # open csv files
import utc
import longlat
import movement
import os
import numpy
import random
import alternativeAlgorithms
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split, KFold
import geopy
import copy
""" Don't forget to install pandas and geopy
Usage path should be set to /~/GPS_Analysis/Manual Algorithm
To run: python3 -i main.py 
"""


if __name__ == "__main__":
    # f = ""
    # file_name = ""
    # print("Welcome!")
    # while len(file_name) == 0  or not(os.path.isfile(f)):
    #     file_name = input("Enter a csv path. Example: \"Baseline Data/D01/3_15091000 Bar 1.CSV\"\nfile path: ") 
    #         # example: 3_15091000 Bar 1.CSV
    #     f = file_name
    #     if len(file_name) == 0:
    #         print("Enter a valid file name")
    #     elif not(os.path.isfile(f)): # file_name = False when no input  
    #         print("\"{}\" is not a valid path. Enter a different path.".format(f))

    f1 = "Baseline Data/F01.csv"
    f2 = "Baseline Data/F02.csv"
    f3 = "Baseline Data/F03.csv"
    f4 = "Baseline Data/F04.csv"
    f5 = "Baseline Data/F05.csv"
    f6 = "Baseline Data/F06.csv"
    NYC = "New Data/NYC.csv"
    bangladesh = "New Data/bangladesh.csv"
    barranquilla = "New Data/barranquilla.csv"
    
    """ ratio of data to use. 0.5 is half the data. 0.1 is 10% of data. 1.0 is 100% of data.
    """
    portion_of_data = 1.0   

    print("Reading CSV: {}".format(bangladesh))
    data = pandas.read_csv(bangladesh)
    # print("Reading CSV: {}".format(f6))
    # data2 = pandas.read_csv(f6)

    utc_time = []
    lattitude = []
    longitute = []
    height = []
    distance_traveled = []
    true_movement = []
    classifierData = []
    for i in range(int(len(data) / portion_of_data)):
        """ Read in data from CSV -  True Movement is for validation purposes. 
        """
        utc_time.append(int(data["TIME"][i]))
        lattitude.append(longlat.convert(str(data["LATITUDE N/S"][i])))
        longitute.append(longlat.convert(str(data["LONGITUDE E/W"][i])))
        height.append(str(data["HEIGHT"][i]))
        true_movement.append(int(data["MOVEMENT"][i])) 
    
    # utc_time2 = []
    # lattitude2 = []
    # longitute2 = []
    # height2 = []
    # distance_traveled2 = []
    # true_movement2 = []
    # classifierData2 =[] 
    # for i in range(int(len(data2) / portion_of_data)): # read and save 2nd data set
    #     utc_time2.append(int(data2["TIME"][i]))
    #     lattitude2.append(longlat.convert(str(data2["LATITUDE N/S"][i])))
    #     longitute2.append(longlat.convert(str(data2["LONGITUDE E/W"][i])))
    #     height2.append(str(data2["HEIGHT"][i]))
    #     true_movement.append(int(data2["MOVEMENT"][i]))


    for i in range(len(utc_time)):
        cluster  = []
        cluster.append(utc_time[i])
        cluster.append(lattitude[i])
        cluster.append(longitute[i])
        cluster.append(height[i])
        classifierData.append(cluster)
        cluster = []
    
    # for i in range(len(utc_time2)): # combine second data set to first data set 
    #     cluster  = []
    #     # cluster.append(utc_time2[i])
    #     cluster.append(lattitude2[i])
    #     cluster.append(longitute2[i])
    #     cluster.append(height2[i])
    #     classifierData.append(cluster)
    #     cluster = []

    """ Sanity check
    """
    # classifierData = []
    # true_movement = []
    # random.seed(87375923)
    # for _ in range(len(utc_time)):
    #     classifierData.append([random.random()])
    #     true_movement.append(random.choice([0, 1]))
    
    """ Shuffle Data
    Probs not the best to do this, cause you loose speed data 
    """
    # c = list(zip(classifierData, true_movement))  
    # random.seed(0) # 0 is seed so work is reproducable  
    # random.shuffle(c) 
    # classifierData, true_movement = zip(*c)

    """ Convert data to numpy arrays
    """
    assert(len(classifierData) != 0)
    classifierData = numpy.array(classifierData)
    classifierData = classifierData.astype(numpy.float64)
    true_movement = numpy.array(true_movement)

    assert(len(classifierData) == len(true_movement))

    kf = KFold(n_splits = 5)
    kf.get_n_splits(classifierData)

    i = 1
    results_RF = []
    for train_indexes, test_indexes in kf.split(classifierData): 
        """ train_indexes contains the list of numpy array of indexes for training and testing data. 
        The first element of train_indexes is the training indexes and the second is the testing. 
        """
        X_train, X_test = classifierData[train_indexes], classifierData[test_indexes]
        y_train, y_test = true_movement[train_indexes], true_movement[test_indexes]

        print("RF Iteration {} of {}...".format(i, 5))
        clf_RF = alternativeAlgorithms.RF(X_train, y_train)
        
        y_pred = clf_RF.predict(X_test)
        print("RF Results:")
        print(confusion_matrix(y_test,y_pred))  
        print(classification_report(y_test,y_pred))  
        print(accuracy_score(y_test, y_pred))
        results_RF.append(accuracy_score(y_test, y_pred))
        i += 1
    print(results_RF)

    i = 1
    results_KNN = []
    for train_indexes, test_indexes in kf.split(classifierData): 
        """ train_indexes contains the list of numpy array of indexes for training and testing data. 
        The first element of train_indexes is the training indexes and the second is the testing. 
        """
        X_train, X_test = classifierData[train_indexes], classifierData[test_indexes]
        y_train, y_test = true_movement[train_indexes], true_movement[test_indexes]

        print("KNN Iteration {} of {}...".format(i, 5))
        clf_KNN = alternativeAlgorithms.KNN(X_train, y_train)
        
        y_pred = clf_KNN.predict(X_test)
        print("KNN Results:")
        print(confusion_matrix(y_test,y_pred))  
        print(classification_report(y_test,y_pred))  
        print(accuracy_score(y_test, y_pred))
        results_KNN.append(accuracy_score(y_test, y_pred))
        i += 1
    print(results_KNN)


    i = 1
    results_SVM = []
    for train_indexes, test_indexes in kf.split(classifierData): 
        """ train_indexes contains the list of numpy array of indexes for training and testing data. 
        The first element of train_indexes is the training indexes and the second is the testing. 
        """
        X_train, X_test = classifierData[train_indexes], classifierData[test_indexes]
        y_train, y_test = true_movement[train_indexes], true_movement[test_indexes]

        print("SVM Iteration {} of {}...".format(i, 5))
        clf_SVM = alternativeAlgorithms.SVM(X_train, y_train)
        
        y_pred = clf_SVM.predict(X_test)
        print("SVM Results:")
        print(confusion_matrix(y_test,y_pred))  
        print(classification_report(y_test,y_pred))  
        print(accuracy_score(y_test, y_pred))
        results_SVM.append(accuracy_score(y_test, y_pred))
        i += 1
    print(results_SVM)

    print("RF:" )
    for result in results_RF:
        print(result)
    print("KNN:" )
    for result in results_KNN:
        print(result)
    print("SVM:")
    for result in results_SVM:
        print(result)

    print("Program Finished")


""" Files 1 & 2 without UTC
RF:
0.9939017979182
0.7468194721900957
1.0
1.0
0.794448533277258
KNN:
1.0
0.5231836820523604
1.0
1.0
0.7540742298391336
SVM:
1.0
0.4672484491641257
1.0
1.0
0.7460834822836715
"""
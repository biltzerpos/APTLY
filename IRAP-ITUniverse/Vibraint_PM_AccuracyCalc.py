"""*************************************************************************************
VIBRAINT PREDICTION MODULE PREDICTOR
THIS PROGRAM GENERATES THE JSON FILE, THE MAIN OUTPUT OF THE PREDICTION MODULE
IT GENERATES THE JSON FILE FOR THE SPECIFIED HOUR AS IN "prediction_time" VARIABLE
JSON FILE CONTAINS THE top 6 MENU ITEMS AND THEIR CORRESPONDING PROBABILITIES
***************************************************************************************
This program also predicts output sequence for a given test sequence, either generated
by program or read from the test_file csv file. It gives the Top accuracy depending upon
the accuracy_level variable which can calculate upto 55 levels of accuracy. 
For reference, model output and individual probabilities for each test sequences are 
updated in the out_target and out_prob csv files
*************************************************************************************"""
#IMPORT THE INITILIZER AND DATA GENERATOR PROGRAMS
import json
import csv
import numpy as np
import pandas as pd
from keras.models import load_model
from datetime import datetime
from Vibraint_PM_Initializer import *
from numpy import argmax
import Vibraint_PM_Initializer as gi
import Vibraint_PM_DataGenerator as dg
from tabulate import tabulate
# load the trained Encoder-Decoder models


import warnings
warnings.filterwarnings("ignore")
# Predicts output sequence for the test sequence and TOP accuracy is calculated
def accuracy_calculate(test_length,infenc,infdec):
    n_samples= test_length
    accuracy_all = list()
    Xtest1, Xtest2, y = dg.get_dataset(n_steps_in, n_steps_out, n_features, n_samples, menu_file, test_file, generate_seq)
    for i in range(n_samples):
        accuracy1 = np.zeros(accuracy_level, dtype=float)
        Xt1 = np.reshape(Xtest1[i],(1,n_steps_in,n_features))
        target = gi.predict_sequence(infenc, infdec, Xt1, n_steps_out, n_features)
        y_list = gi.one_hot_decode(y[i])
        target_list = gi.one_hot_decode1(target,n_features)
        for i in range(n_steps_in-1):
            for j in range(accuracy_level):
                if y_list[i] == target_list[i][j]:
                    accuracy1[j]+=1
        for k in range(1,accuracy_level):
            accuracy1[k] +=accuracy1[k-1]
        accuracy_all.append(accuracy1)
    accuracy_final = np.zeros(accuracy_level, dtype=float)
    for j in range(accuracy_level):
    	for i in range(n_samples):
    		accuracy_final[j] +=accuracy_all[i][j]
    accuracy_final= (accuracy_final/((n_steps_in-1)*(n_samples)))*100
#    print(accuracy_final)
    return accuracy_final

models= [1000,10000,100000,500000,1000000]
test_length = [100,500,1000]
acc_cal = list()
with open(acc_file, 'w', newline="") as accFile:
	writer = csv.writer(accFile,delimiter =',')
	for test in test_length:
		print('**************************************************************************')
		print("Number of Test Sequences :",test)
		for model in models:
			enc = 'encoder'+str(model)+'.h5'
			dec = 'decoder'+str(model)+'.h5'
			infenc = load_model(enc)
			infdec = load_model(dec)
			acc_cal1 = accuracy_calculate(test,infenc,infdec)
			print("Model:",model)
			print("Top 5 Accuracy:",acc_cal1)
			writer.writerow(acc_cal1)
			acc_cal.append(acc_cal1)
		print('**************************************************************************')





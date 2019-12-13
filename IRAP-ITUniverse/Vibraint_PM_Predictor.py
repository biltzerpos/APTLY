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

# load the trained Encoder-Decoder models
infenc = load_model('encoder.h5')
infdec = load_model('decoder.h5')

# Predicts output sequence for the test sequence and TOP accuracy is calculated
accuracy1 = np.zeros(accuracy_level, dtype=float)
Xtest1, Xtest2, y = dg.get_dataset(n_steps_in, n_steps_out, n_features, n_samples, menu_file, test_file, generate_seq)
with open(out_target, 'w', newline="") as writeFile:
	writer = csv.writer(writeFile,delimiter =',')
	for i in range(n_samples):
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
		writer.writerow(target)
print("Expected Output")
print(y_list)
print("Actual Output")
print(gi.one_hot_decode(target))
accuracy1 = (accuracy1/((n_steps_in-1)*(n_samples)))*100
print("Top", accuracy_level,"Accuracy")
print(accuracy1)

Sum = np.zeros(n_features-2, dtype=float)
Predicted_menu = []
Predicted_prob = []
with open(out_target, 'r', newline="") as read_file:
	reader = csv.reader(read_file,delimiter =',')
	with open(out_prob, 'w', newline="") as write_file:
		writer = csv.writer(write_file,delimiter =',')
		for read in reader:
			df = pd.DataFrame(read)
			test = df.iloc[prediction_time]
			test = (test[0].split(" "))
			t1= test[0].split("[")
			test[0] = t1[1]
			t2= test[56].split("]")
			test[56] = t1[1]
			final_list = []
			for i in test:
				final_list.append(i.strip())
			writer.writerow(final_list)
			for i in range(n_features-2):
				Sum[i] = Sum[i]+float(test[i])
Average1 = Sum/n_samples
Prob_list= np.argsort(Average1)[::-1][:n_features-2]
df1 = pd.read_csv(menu_file)
for i in range(n_features-2):
	for j in range(n_features-3):
		if df1['index'][j] == Prob_list[i]:
			Predicted_menu.append(int(df1['selectionId'][j]))
			Predicted_prob.append(float(Average1[Prob_list[i]]))
print("Top Menu Items are", Predicted_menu[:num_predict])
print("Top Menu Items are", Predicted_prob[:num_predict])

outputData = gi.generate_json(Predicted_menu,Predicted_prob)
with open(output_file, "w") as output1:
	json.dump(outputData, output1)

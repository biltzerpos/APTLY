"""******************************************************************************************
VIBRAINT PROJECT - INITIALIZER
THIS IS AN Initializer PROGRAM, WHERE VARIABLES ARE ASSIGNED AND COMMON FUNCTIONS ARE DEFINED
THIS PROGRAM IS USED BY ALL THE REMAINING PROGRAMS OF THE PROJECT
FEW VARIABLES NEEDS USER INPUTS BEFORE ANY OTHER PROGRAM IS EXECUTED, ELSE DEFAULT VALUES 
WOULD BE CONSIDERED
******************************************************************************************"""
import numpy as np
from numpy import argmax
from datetime import datetime
"""Please update below variables before running the program"""
# Path where all the csv files are stored
file_path= 'C:/Users/amitb/Documents/Ganesha/VIBRAINT Project/OutputFiles/'
# this represents an hour in 24 hrs; this could range from 0 to 23;
prediction_time = 1
# Specify 1 if you want program to generate synthetic data, 
# else 0 where it will read from the corresponding train_seq or test_seq sequnce csv files
generate_seq =1
# number of samples you want to generate or number of samples in the file
n_samples = 1
# Level of accuracy required, if =3, then program would give Top 3 accuracy
accuracy_level = 5
# number of predictions or number of menu items to be predicted
num_predict = 6
n_features = 55 + 2
n_steps_in = 24+1
print("init file")
n_steps_out = 24+1
n_units = 512
#json file variables
messageId = 156
messageType = 'Prediction'
userId = 5
# current date and time
now = datetime.now()
timestamp = datetime.timestamp(now)
timestamp = int(timestamp)
#Model Hyper parameters
epochs = 1
loss = 'categorical_crossentropy'
optimizer = 'adam'
activation = 'softmax'

# all csv Files and Json file
menu_file = file_path + 'Menu.csv'
input_file = file_path + 'Vibraint_TrainSequences.csv'
json_file = file_path + 'Vibraint_GenerateJsonFiles.csv'
out_prob = file_path + 'Vibraint_OutputProbabilities.csv'
test_file = file_path + 'Vibraint_TestSequence.csv'
output_file = file_path+'Vibraint_PM_Output.json'
out_target = file_path + 'Vibraint_OutputTarget.csv'


#"""This function predicts the probabilities for the test sequences provided"""
def predict_sequence(infenc, infdec, source, n_steps, n_features):
	# encode
	state = infenc.predict(source)
	# start of sequence input
	target_seq = np.array([0.0 for _ in range(n_features)]).reshape(1, 1, n_features)
	# collect predictions
	output = list()
	for t in range(n_steps):
		# predict next item
		yhat, h, c = infdec.predict([target_seq] + state)
		# store prediction
		output.append(yhat[0,0,:])
		# update state
		state = [h, c]
		# update target sequence
		target_seq = yhat
	return np.array(output)

#Generate json file
def generate_json(Predicted_menu,Predicted_prob):
	outputData = {}
	outputData = {
	"messageId":messageId,
	"messageType":messageType,
	"messageData":{
	"userId":userId,
	"timestamp":timestamp,
	"messageData":{
		"ids":[Predicted_menu[0],Predicted_menu[1],Predicted_menu[2],Predicted_menu[3],Predicted_menu[4],Predicted_menu[5]],
		"values":[Predicted_prob[0],Predicted_prob[1],Predicted_prob[2],Predicted_prob[3],Predicted_prob[4],Predicted_prob[5]]}
		}
	}
	return outputData

# decode a one hot encoded string
def one_hot_decode(encoded_seq):
	return [argmax(vector) for vector in encoded_seq]
def one_hot_decode1(encoded_seq,n_features):
	return [np.argsort(vector)[::-1][:n_features-2] for vector in encoded_seq]
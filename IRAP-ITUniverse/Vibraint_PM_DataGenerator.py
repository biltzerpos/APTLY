"""******************************************************************************************
VIBRAINT PROJECT - DATA GENERATOR
THIS IS A DATA GENERATOR PROGRAM, WHICH CAN GENERATE A RANDOM SEQUENCES OF LENGTH n_steps_in
BASED ON THE PROBABILITIES SPECIFIED IN THE MENU CSV FILE. IT GENERATES n_samples NUMBER
OF SEQUENCES. 
ALSO, GENERATED SEQUENCES ARE WRITTEN IN CORRESPONDING input_seq CSV FILES
OUTPUT FROM THIS PROGRAM ARE THE SOURCE AND EXPECTED OUTPUT VALUES IN AN ONE-HOT-ENCODED ARRAY
******************************************************************************************"""
#IMPORT THE INITILIZER PROGRAM
import Vibraint_PM_Initializer as gi
import numpy as np
import pandas as pd
from random import choices
import csv
from keras.utils import to_categorical

# generate a sequence 
def generate_sequence(length, n_samples,menu_file,input_seq):
	df = pd.read_csv(menu_file)
	length = int(length/4)
	with open(input_seq, 'w', newline="") as writeFile:
		writer = csv.writer(writeFile,delimiter =',')
		for _ in range(n_samples):
			seq = np.zeros(length,dtype=int)
			seq1 = np.zeros(length,dtype=int)
			seq2 = np.zeros(length,dtype=int)
			seq3 = np.zeros(length,dtype=int)
			seq4 = np.zeros(length,dtype=int)
			seq1 = choices(df['selectionId'], df['Morning'], k=6)
			seq2 = choices(df['selectionId'], df['Noon'], k=6)
			seq3 = choices(df['selectionId'], df['Evening'], k=6)
			seq4 = choices(df['selectionId'], df['Night'], k=6)
			seq = seq1+seq2+seq3+seq4
			writer.writerow(seq)
	writeFile.close()

def get_dataset(n_in, n_out, cardinality, n_samples,menu_file,input_seq, generate_seq):
	X1, X2, y = list(), list(), list()
	seq = np.zeros(n_in-1,dtype=int)
	bos = [55]
	eos = [56]
	df = pd.read_csv(menu_file)
	if generate_seq == 1:
		generate_sequence(n_in-1,n_samples,menu_file,input_seq)
	with open(input_seq, 'r', newline="") as readFile:
		reader = csv.reader(readFile,delimiter =',')
		for read in reader:
			for i in range(n_in-1):
				test = int(read[i])
				for j in range(cardinality-3):
					if (df['selectionId'][j] == test):
						seq[i] = df['index'][j]
			source = seq
			source = np.squeeze(source)
			target = np.append(source[:n_out-1],eos)
			source = np.append(bos,source)
			target_in = np.append(bos,target[:-1])
			src_encoded = to_categorical(source, num_classes=cardinality)
			tar_encoded = to_categorical(target, num_classes=cardinality)
			tar2_encoded = to_categorical(target_in, num_classes=cardinality)
		# store
			X1.append(src_encoded)
			X2.append(tar2_encoded)
			y.append(tar_encoded)
	return np.array(X1), np.array(X2), np.array(y)
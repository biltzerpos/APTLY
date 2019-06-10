############
## README ##
############

# The scripts in this folder were created by Ricardo Reimao
# They are used to extract *AVERAGE* audio features from audio files in a folder
# This is useful for doing TRADITIONAL machine learning analysis, using WEKA
# Example: Extract the average STFT (which is a vector) for each audio file in a folder.
# The script requirements (and more detailed documentation) can be found in each script


# Example of run:    $ python folder_stft.py ~/Desktop/dataset/class1 output_file_class1.csv class1
# This would generate a file like:
# 1.56,3.561,7.8412,3.78,...,1.67,class1
# [...]
# 1.45,6.2345,4.321,7.12,...,5.61,class1


# Do the same for each class, and you will have one CSV file per class. 
# Merge the files, and you will have a big CSV file with all the classes and extracted features.
# This CSV file can be input into Weka

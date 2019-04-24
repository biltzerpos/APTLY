
from PIL import Image
from PIL import ImageChops
import os
import pandas as pd
import numpy as np
import sys
import subtract

def exit_script():
    print ("""This Script takes 4 parameters.
The first is the path which contains original sound clips in bitmap form with just an id number as the name. 
The second argument is the path which contains all of the edited bitmaps.
These bitmaps should be in the form <id-frequency-Q value-Gain in dB.bmp>.
The third parameter is the destination folder which should exist. 
The files returned will be the subtracted differences with the same name as the edited files provided.
The fourth parameter takes an integer and corresponds to what kind of subtraction you would like to do:

1 for absolute difference\n
2 for original - edited\n
3 for edited - original 

""")
    sys.exit()

if len(sys.argv) < 4:
    exit_script()
    
#orig_path = '../p/Original/'
#eqd_path = '../p/EQed/'
#destination = '../p/Difference/'

orig_path = sys.argv[1]
eqd_path = sys.argv[2]
destination = sys.argv[3]
try:
    sub_type = int(sys.argv[4])
except:
    exit_script()

#Check if pparmeters are formatted correctly
if not (os.path.isdir(orig_path) and os.path.isdir(eqd_path) and os.path.isdir(destination)):
    exit_script()
if sub_type > 3 or sub_type < 1:
    exit_script()

#Destination shold end with /
if destination[-1] != "/":
    destination = destination + "/"
    
#Make a data frame with all the information needed for each file for easy acces of information for each sound file
#Indexed by id and corresponding paths are column entries for each piece of audio
cols = ['id', 'freq', 'q', 'dB', 'orig_path', 'eqd_path']
data = pd.DataFrame(columns=cols)

for idx, filename in enumerate(os.listdir(eqd_path)):
    eq_path = os.path.join(eqd_path, filename)
    filename = filename.replace('--', '-n')#Some files have double dashes for negative. Replace with n for negative
    params = filename.split('-')
    params[-1] = params[-1][:-4] #Remove '.bmp'

    if params[2] != '0':  #Some files don't have all the parameters in the name 
        params[2] = params[2][:-1]   #Remove 'q'
    else:
        params.insert(3, '0')
    orig_id_path = os.path.join(orig_path,(params[0]+'.bmp'))
    if os.path.exists(orig_id_path):
        params.insert(4, orig_id_path)
    else:
        continue
    params.insert(5, eq_path)
    data.loc[idx] = params
data = data.sort_values('id').reset_index()

if data.empty:
    print("\nMake sure that your paths are correct... Couldn't find matching spectograms\n")
    exit_script()


for ind, row in data.iterrows():
    
    if not os.path.exists(row['orig_path']):
        print("Could not find corresponding original spectogram for " + row['id'])
        continue
    
    result = subtract.subtract(row['orig_path'], row['eqd_path'], sub_type)

    #if sub_type == 1:
    #    result = ImageChops.difference(original, equalized) #Returns absolute value of the differences in the image
    #elif sub_type == 2:
    #    result = ImageChops.subtract(original, equalized) #Subtracts 
    #elif sub_type == 3:
    #    result = ImageChops.subtract(equalized, original)
    
    filepath = destination + row['id'] + '-' + row['freq'] + '-' + row['q'] + 'q-' + row['dB']
    try:
        result.save(filepath + ".bmp")
    except:
        print ("Error")
        sys.exit()

    
    

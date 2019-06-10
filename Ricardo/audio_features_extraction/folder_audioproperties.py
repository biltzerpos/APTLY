#########
### Script developed by Ricardo Reimao (Jan 7, 2019)
### The script exctracts audio timbre models from an audio file. This includes: brightness, hardness, depth and roughness.
### The script uses the timbral models library. More information can be found at: https://www.audiocommons.org/2018/07/15/audio-commons-audio-extractor.html
### The library code can be found at: https://github.com/AudioCommons/timbral_models , but you can simply do: pip install timbral_models
#########
### The first argument is the folder containing the audio files
### The second argument is the Class of the file (real or fake)
### The third argument is the output csv file
#########

import timbral_models as tm
import sys
from pathlib import Path

pathlist = Path(sys.argv[1]).glob('**/*.wav')
output_file_path = sys.argv[3]
output_file = open(output_file_path, "a+")
class_folder = sys.argv[2]


## Writing headers on the output file
output_file.write("brightness,hardness,depth,roughness,class\r\n")

#Loop through the folder doing the calculations
for path in pathlist:
    path_in_str = str(path)
    print(path_in_str)
    
    brightness = tm.timbral_brightness(path_in_str)
    hardness = tm.timbral_hardness(path_in_str)
    depth = tm.timbral_depth(path_in_str)
    roughness = tm.timbral_roughness(path_in_str)
    
    output_file.write(str(brightness) + ',' + str(hardness) + ',' + str(depth) + ',' + str(roughness) + ',' + class_folder + '\r\n')

output_file.close()
print("Done!")

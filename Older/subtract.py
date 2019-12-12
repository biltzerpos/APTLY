from PIL import Image
from PIL import ImageChops
import os
import sys

def exit_script():
    print("""This script takes 4 parameters. The first 2 are the paths for the respective images 
to be subtracted from each other.The third parameter is the type of subtraction you would like to do. To do absolutedifference set flag to 1, set 2 for subtracting Img1 from Img2 and anything else will subtract Image2 from Image1
The 4th parameter is the output file""")
    sys.exit()

def subtract(Image1_path, Image2_path, sub_type):
    if not(os.path.exists(Image1_path)) or not(os.path.exists(Image2_path)):
        exit_script()

    try:
        Image1 = Image.open(Image1_path)
        Image2 = Image.open(Image2_path)
    except:
        print("\nError openng the images")
        sys.exit()



    try:
        sub_type = int(sub_type)
    except:
        print("please input an integer as the 3rd argument")
        sys.exit()

    result =""

    if sub_type == 1:
        result = ImageChops.difference(Image1, Image2)
    elif sub_type == 2:
        result = ImageChops.subtract(Image1, Image2)
    else:
        result = ImageChops.subtract(Image2, Image1)

    return result
    

if __name__ == "__main__":
    
    if len(sys.argv) < 4:
        exit_script()

    Sub_img = subtract(sys.argv[1], sys.argv[2], sys.argv[3])
    
    Sub_img.save(sys.argv[4])

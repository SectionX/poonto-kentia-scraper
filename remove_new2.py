from multiprocessing import Pool
from time import perf_counter
import os
from PIL import Image

imagedir = f'{os.getcwd()}\\images'
outputdir = f'{os.getcwd()}\\test_images1'

imagelist = os.listdir(imagedir)

def mainfunc():
    for z in range(51):
        img = Image.open(f"{imagedir}\\{imagelist[z]}")
        row = 40
        column = 40
        for i in range(10):
            for y in range(10):
                pixel = img.getpixel((row+y,column+i))
                flag = False
                if (225 <= pixel[0] and pixel[0] <= 232) and (2 <= pixel[1] and pixel[1] <= 10) and (120 <= pixel[2] and pixel[2] <= 130): 
                    flag = True
                else: break
        print(flag)
        if not flag: pass
        img.close()
    
    # print(list(img.getdata())[row+column])


def main(): pass


if __name__ == '__main__':
    mainfunc()
from PIL import Image
import os
from time import perf_counter
from multiprocessing import Pool


def checkNEW(img):
    row = 40
    column = 40
    flag = False
    try:  #checks for a specific magenta'ish color to determine if the "NEW" stamp exists.
        for i in range(10):
            for y in range(10):
                pixel = img.getpixel((row+y,column+i))
                if (225 <= pixel[0] and pixel[0] <= 232) and (2 <= pixel[1] and pixel[1] <= 10) and (120 <= pixel[2] and pixel[2] <= 130): 
                    flag = True
                else: break
    except: return "Err"
    return flag


def cropper(img):
    try:
        cropbox = (0, 147, img.width, img.height) #left, upper, right, lower
        img = img.crop(cropbox)
    except:
        with open("log_cropimagefail.txt", 'a') as f: f.write(f"Failed to crop {img=}\n")
        return "Err"
    return img



def processImage(image):
    try:
        img = Image.open(f".\\images\\{image}")
    except:
        with open("log_cropimagefail.txt", 'a') as f: f.write(f"Failed to open {image=}\n")
        return
    
    flag = checkNEW(img)
    if flag == "Err": 
        return
    elif flag:
        img = cropper(img)
        if img == "Err": return

    img.save(f"{os.getcwd()}\\processed\\{image}")

    img.close()



def main(threads):
    imagelist = os.listdir(os.getcwd()+"\\images")
    with Pool(threads) as pool:
        pool.map(processImage, imagelist)


if __name__ == '__main__':
    start = perf_counter()
    main(4)
    print(perf_counter()-start)
        



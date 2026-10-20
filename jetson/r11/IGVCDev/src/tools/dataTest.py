import csv
import torch
import numpy as np
from PIL import Image
import time
import pandas as pd
import sys
import pickle
import zlib
import base64
import h5py
import array





def appendCSV(dataFile, data):
    with open(dataFile, 'a', newline='\n') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def readRowCSV(dataFile, index):
    with open(dataFile, 'r') as file:
        reader = csv.reader(file)

        # Option 1: Iterate to the desired row
        for i, row in enumerate(reader):
            if i == index:  # Row index is zero-based
                return row

        # If no return happened in the loop, the row index was out of range
        return None
    
def getValuesRow(dataFile, index):
    width = 320
    height = 240
    channel = 3
    imageShape = width*height*channel
    cam0 = []
    cam1 = []
    row = readRowCSV(dataFile, index)
    steering = float(row[0])
    throttle = float(row[1])
    for index, data in enumerate(row):
        if index > 1 and index < imageShape+2:
            cam0.append(data)
        elif index >= imageShape+2:
            cam1.append(data)
    
    # cam0 = np.array(cam0)
    # cam0 = cam0.reshape(height, width, channel)
    # cam1 = np.array(cam1)
    # cam1 = cam1.reshape(height, width, channel)

    return steering, throttle, cam0, cam1

def crop(img, crop):
    left = crop[0]*img.width
    top = crop[1]*img.height
    right = crop[2]*img.width
    bottom = crop[3]*img.height
    return img.crop((left, top, right, bottom))

def flatten(image):
    return [item for sublist in image for item in sublist]

def main():
    dataFile = "training_data.csv"

    steering, throttle, cam0, cam1 = getValuesRow(dataFile, 0)
    # data = [steering + throttle + cam0 + cam1]
    

    # pixels0 = np.array(cam0, dtype=np.uint8)
    # img0 = Image.fromarray(pixels0, 'RGB')

    data = list(readRowCSV(dataFile, 0))
    # cam0 = data[2]
    # cam0 = np.reshape(240, 320, 3)
    # pixles = np.array(cam0, dtype=np.uint8)
    # cam0 = Image.fromarray(pixles)
    # cam0.save('readFile.jpg')
    # newData = pickle.dumps(data)
    # newData = zlib.compress(newData)
    # newData = base64.b64encode(newData).decode('utf-8')

    cam0 = np.array(cam0)
    cam0 = cam0.reshape(240, 320, 3)
    pixles = np.array(cam0, dtype=np.uint8)
    cam0 = Image.fromarray(pixles)
    cam0 = crop(cam0, (0, 0.4, 1, 0.8))
    cam0 = np.array(cam0)
    cam0 = cam0.flatten().tolist()
    # cam0 = array.array('i', cam0)

    cam1 = np.array(cam1)
    cam1 = cam1.reshape(240, 320, 3)
    pixles1 = np.array(cam0, dtype=np.uint8)
    cam1 = Image.fromarray(pixles1)
    cam1 = crop(cam1, (0, 0.4, 1, 0.8))
    cam1 = np.array(cam1)
    cam1 = cam1.flatten().tolist()
    # cam1 = array.array('i', cam1)


    # steering = np.array(steering)
    # throttle = np.array(throttle)
    
    newData = [steering] + [throttle] + cam0 + cam1

    


    print(f"Data Length: {len(data)}")
    print(f"Data Size: {sys.getsizeof(data)}")
    print(f"Data Length: {len(newData)}")
    print(f"Data Size: {sys.getsizeof(newData)}")

    start = time.time()
    appendCSV(dataFile, [data])
    end = time.time()
    print(f"Time to save without optimization: {end-start}")

    start = time.time()
    appendCSV(dataFile, [newData])
    end = time.time()
    print(f"Time to save with optimization: {end-start}")

    # start = time.time()
    # with h5py.File('data.h5', 'w') as f:
    #     f.create_dataset('dataset', data=newData)
    # end = time.time()
    # print(f"Time to save with optimization: {end-start}")





if __name__ == '__main__':
    main()
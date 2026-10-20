#!/usr/bin/env python3 
import os
import glob
import shutil

def rename_images(root_directory, targetName, dest, camera):
    # Get a list of all .jpg files in the root directory and its subdirectories
    jpg_files = glob.glob(os.path.join(root_directory,'*.jpg'))

    for jpg_file in jpg_files:
        # Generate the new filename
        count = jpg_files.index(jpg_file)
        new_filename = f"{targetName}_{camera}_{count}.jpg"

        # Construct the new file path
        new_filepath = os.path.join(root_directory,new_filename)

        # Rename the file
        os.rename(jpg_file, new_filepath)

        # move renamed file to destination dir
        shutil.copy(new_filepath,os.path.join(dest,new_filename))

# given the root, destination, and current camera used 
# this will recursively rename and move every picture located within the /data/cam*/{timestap}/ directories
def moveImages(root, dest, camera):
    dirs = os.listdir(root)
    # dirs = sorted(dirs, key=lambda x: int(x.split("_")[-1].split(".")[0]))
    for dir in dirs:
        target = os.path.join(root,dir)
        rename_images(target,dir,dest,camera)           

# given the root, dest, and type of data append the collect information to a central location 
# for a greater data collection
def moveData(root,dest, type):
    targetFileName = ""
    if type == "steering":
        targetFileName = f'{dest}/steering_data.txt'
    elif type == "throttle":
        targetFileName = f'{dest}/throttle_data.txt'
    else:
        print("Cannot find steering or throttle directory")

    # Handle file creation if target .txt file does not already exist
    if not os.path.exists(targetFileName):
        try:
            with open(targetFileName, 'w') as file:
                print(f"File successfully create: {targetFileName}")
        except Exception as e:
            print(f"An error occured while creating the file: {e}")
    else:
        print(f"The file already exist: {targetFileName}")


    txtFiles = glob.glob(os.path.join(root,'*.txt'))

    # go through every txt file copy its content and append it to the data file in /data/training
    for txt in txtFiles:
        with open(txt, 'r') as txtFile:
            data = txtFile.read()

            with open(targetFileName, 'a') as targetTxtFile:
                targetTxtFile.write(data)
    

# Give a root of the images capture and a destination this will rename and move the images over. 
# root and dest are defaulted to the autoNN/data/dir
def transferData(root=f'/home/{os.getlogin()}/IGVCDev/src/autoNN/data/', dest=f'/home/{os.getlogin()}/IGVCDev/src/autoNN/data/training/'):

    subDirs = sorted(os.listdir(root))

    for dir in range(0,4):
        targetDir = os.path.join(root,subDirs[dir])
        destination = os.path.join(dest,subDirs[dir])
        if(dir < 2):
            moveImages(targetDir, destination, subDirs[dir])
        else:
            moveData(targetDir, destination, subDirs[dir])


if __name__ == "__main__":
  # Specify the root directory
    root_directory = f'/home/{os.getlogin()}/IGVCDev/src/autoNN/data'
    destination_directory = f'/home/{os.getlogin()}/IGVCDev/src/autoNN/data/training'
    cam0Path = f"{destination_directory}/cam0"
    cam1Path = f"{destination_directory}/cam1"
    steeringPath = f"{destination_directory}/steering"
    throttlePath = f"{destination_directory}/throttle"

    if not os.path.exists(root_directory):
        os.mkdir(root_directory)
        os.mkdir(destination_directory)
        os.mkdir(cam0Path)
        os.mkdir(cam1Path)
        os.mkdir(steeringPath)
        os.mkdir(throttlePath)

    elif not os.path.exists(destination_directory):
        os.mkdir(destination_directory)
        os.mkdir(cam0Path)
        os.mkdir(cam1Path)
        os.mkdir(steeringPath)
        os.mkdir(throttlePath)
    
    if not os.path.exists(cam0Path):
        os.mkdir(cam0Path)

    if not os.path.exists(cam1Path):
        os.mkdir(cam1Path)

    if not os.path.exists(steeringPath):
        os.mkdir(steeringPath)

    if not os.path.exists(throttlePath):
        os.mkdir(throttlePath)

    # Call the function to rename the images
    transferData(root_directory)
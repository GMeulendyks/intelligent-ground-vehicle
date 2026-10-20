import os
import glob
from PIL import Image

'''
Write a function that takes a directory as input and prints a list of all
the file names.
'''
def names(path):
    files = os.listdir(path)
    sorted_files = sorted(files, key=lambda x: int(x.split("_")[-1].split(".")[0]))
    for file in sorted_files:
        print(file)

def flipImages(path):
    # Directory containing the images
    directory = path

    # List all files in the directory
    files = os.listdir(directory)

    # Filter out only the image files with the desired naming convention
    image_files = [file for file in files if file.startswith("Camera_") and file.endswith(".jpg")]

    # Sort the image files based on the index
    image_files.sort(key=lambda x: int(x.split("_")[-1].split(".")[0]))

    # Process each image
    for image_file in image_files:
        # Open the image
        image_path = os.path.join(directory, image_file)
        image = Image.open(image_path)

        # Flip the image horizontally
        flipped_image = image.transpose(Image.FLIP_LEFT_RIGHT)

        # Construct the filename for the flipped image
        parts = image_file.split("_")
        ID = parts[1]
        index = parts[-1].split(".")[0]
        flipped_image_file = f"Camera_{ID}_Frame_{index}_flipped.jpg"

        # Save the flipped image to the directory
        flipped_image_path = os.path.join(directory, flipped_image_file)
        flipped_image.save(flipped_image_path)

        print(f"Flipped image saved: {flipped_image_path}")

    # Re-list all files in the directory after flipping
    files = os.listdir(directory)

    # Filter out only the flipped image files with the desired naming convention
    flipped_image_files = [file for file in files if file.startswith("Camera_") and file.endswith("_flipped.jpg")]

    # Sort the flipped image files based on the index
    flipped_image_files.sort(key=lambda x: int(x.split("_")[-2]))

    # Renaming the flipped images sequentially to match the original order
    for i, flipped_image_file in enumerate(flipped_image_files):
        # Construct the filename for the original image
        parts = flipped_image_file.split("_")
        ID = parts[1]
        index = parts[-2]
        original_index = int(index) + len(image_files)
        original_image_file = f"Camera_{ID}_Frame_{original_index}.jpg"

        # Rename the flipped image file
        os.rename(os.path.join(directory, flipped_image_file), os.path.join(directory, original_image_file))

        print(f"Flipped image renamed: {os.path.join(directory, original_image_file)}")

def makeDirs():
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


def append_negated_values(input_file):
    # Read the contents of the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Extract numerical values and negate them
    values = [float(line.strip()) for line in lines]
    negated_values = [-value for value in values]

    # Append negated values to the end of the file
    with open(input_file, 'a') as file:
        for value in negated_values:
            file.write(f"{value}\n")

def duplicate_values(input_file):
    # Read the contents of the input file
    with open(input_file, 'r') as file:
        lines = file.readlines()

    # Append duplicated values to the end of the file
    with open(input_file, 'a') as file:
        for line in lines:
            file.write(line)

def main():
    root_directory = f'/home/{os.getlogin()}/IGVCDev/src/autoNN/data'
    destination_directory = f'/home/{os.getlogin()}/IGVCDev/src/autoNN/data/training'
    cam0Path = f"{destination_directory}/cam0"
    cam1Path = f"{destination_directory}/cam1"
    steeringPath = f"{destination_directory}/steering"
    throttlePath = f"{destination_directory}/throttle"
    # Check to make sure all the directories are present
    # makeDirs()

    flipImages(cam0Path)
    flipImages(cam1Path)
    append_negated_values(steeringPath + "/steering_data.txt")
    duplicate_values(throttlePath + "/throttle_data.txt")

    # Copy all the files from /cam0 to /training/cam0 with the updated index


    # names("/home/igvc/IGVCDev/src/data_collection_ws/data/cam0/24-03-23-05_17_27")

if __name__ == '__main__':
    main()
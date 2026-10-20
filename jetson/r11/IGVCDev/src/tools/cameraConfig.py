import cv2
import subprocess
import yaml # pip install PyYAML
import os

def find_available_cameras(max_tests=10):
    available_cameras = []
    for i in range(max_tests):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
    return available_cameras


def get_device_id(device_path):
    try:
        # Execute the udevadm command and capture its output
        output = subprocess.check_output(["udevadm", "info", "--query=all", "--name=" + device_path])
        output = output.decode('utf-8')  # Decode byte string to a regular string
        
        # Initialize an empty dictionary to store the IDs
        device_ids = {}
        
        # Look for lines containing the vendor and model IDs
        for line in output.split('\n'):
            if 'ID_VENDOR_ID' in line:
                device_ids['vendor_id'] = line.split('=')[1]
            elif 'ID_MODEL_ID' in line:
                device_ids['model_id'] = line.split('=')[1]
                
        return device_ids
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def loadCameraConfig():
    with open(f"/home/{os.getlogin()}/IGVCDev/src/data_collection_ws/config/cameraConfig.yaml", 'r') as file:
        data = yaml.safe_load(file)

    # Left camera assignments
    leftCamera_vendorID = data["cameraIDs"]["leftCamera"]["vendor_id"]
    leftCamera_modelID = data["cameraIDs"]["leftCamera"]["model_id"]
    leftCameraID = {"vendor_id": f"{leftCamera_vendorID}", "model_id": f"{leftCamera_modelID}"}
    
    # Right camera assignments
    rightCamera_vendorID = data["cameraIDs"]["rightCamera"]["vendor_id"]
    rightCamera_modelID = data["cameraIDs"]["rightCamera"]["model_id"]
    rightCameraID = {"vendor_id": f"{rightCamera_vendorID}", "model_id": f"{rightCamera_modelID}"}

    return leftCameraID, rightCameraID

def updateCameraConfigs(leftCamera, rightCamera):
    with open(f"/home/{os.getlogin()}/IGVCDev/src/data_collection_ws/config/leftCamera.yaml", 'r') as file:
        data = yaml.safe_load(file)
    data["/**"]["ros__parameters"]["video_device"] = leftCamera
    with open(f"/home/{os.getlogin()}/IGVCDev/src/data_collection_ws/config/leftCamera.yaml", 'w') as file:
        yaml.safe_dump(data, file)

    with open(f"/home/{os.getlogin()}/IGVCDev/src/data_collection_ws/config/rightCamera.yaml", 'r') as file:
        data = yaml.safe_load(file)
    data["/**"]["ros__parameters"]["video_device"] = rightCamera
    with open(f"/home/{os.getlogin()}/IGVCDev/src/data_collection_ws/config/rightCamera.yaml", 'w') as file:
        yaml.safe_dump(data, file)

def run():
    
    # load the camera configuration file
    leftCameraID, rightCameraID = loadCameraConfig()
    cameraIDs = [
        leftCameraID,
        rightCameraID
    ]

    # Find available camera indexes
    cameras = find_available_cameras()
    print("Available camera indices:", cameras)

    # Determine the device ID of camera found at each index
    cam0 = f"/dev/video{cameras[0]}"
    cam1 = f"/dev/video{cameras[1]}"
    cam0_id = get_device_id(cam0)
    cam1_id = get_device_id(cam1)
    IDs = [
        [cam0_id, cam1_id],
        [cam0, cam1]
    ]
    print(f"{cam0} ID: {cam0_id}")
    print(f"{cam1} ID: {cam1_id}")

    # Assign the proper camera to the given index
    leftCamera = None
    rightCamera = None
    for index, id in enumerate(IDs[0], start=0):
        leftCamera = f"/dev/video{cameras[index]}" if id  == cameraIDs[0] else leftCamera
        rightCamera = f"/dev/video{cameras[index]}" if id == cameraIDs[1] else rightCamera

    # Update the camera config files
    updateCameraConfigs(leftCamera, rightCamera)


if __name__ == '__main__':
    run()
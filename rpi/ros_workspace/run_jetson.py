import os
import subprocess
import sys
import time


def terminate(processes):
    for proc in processes:
        try:
            proc.terminate()
            proc.wait(timeout=1)
        except:
            proc.kill()


def main():
    current_dir = os.getcwd()
    environment = os.environ.copy()

    processes = []

    if "--test" in sys.argv:
        environment["TEST_IMG_PATH"] = (
            current_dir + "/src/test_data_providers/res/test_img.jpg"
        )
        # This one is specific to my (Jared) own environment
        # but if you train it with the output being output.pth, this'll work
        environment["NN_MODEL"] = current_dir + "/little_blue_v2.pth"
        environment["PACKAGER_CONF"] = current_dir + "/src/packager/config/test.yaml"
        processes.append(
            subprocess.Popen(
                ["ros2", "launch", "test_data_providers", "launch.py"], env=environment
            )
        )
        processes.append(
            subprocess.Popen(
                ["ros2", "launch", "arduino_control", "launch_testing.py"],
                env=environment,
            )
        )
        processes.append(
            subprocess.Popen(
                [
                    "ros2",
                    "run",
                    "gps_hack",
                    "gps_talker",
                ],
                env=environment,
            )
        )
    elif "--packager_only" in sys.argv:
        environment["PACKAGER_CONF"] = current_dir + "/src/packager/config/default.yaml"
        environment["DATA_COLLECTION_PATH"] = "/usr/local/data_collection"
    else:
        environment["NN_MODEL"] = current_dir + "/little_blue_v2.pth"
        environment["PACKAGER_CONF"] = current_dir + "/src/packager/config/default.yaml"
        environment["DATA_COLLECTION_PATH"] = "/usr/local/data_collection"
        arducam_config_path = current_dir + "/src/packager/config/arducam_configs"
        processes.extend(get_full_processes(arducam_config_path, environment))

    processes.append(
        subprocess.Popen(
            ["ros2", "launch", "igvc_nn", "launch_node.py"], env=environment
        )
    )

    processes.append(
        subprocess.Popen(["ros2", "launch", "packager", "launch.py"], env=environment)
    )

    processes.append(
        subprocess.Popen(
            ["ros2", "launch", "data_collector", "launch.py"], env=environment
        )
    )

    processes.append(
        subprocess.Popen(
            ["ros2", "run", "gps_node", "gps_node"], env=environment
        )
    )
    # AI nodes down the line too

    # wait until keyboard interrupt or one of them dies and exit
    try:
        while True:
            for p in processes:
                if p.poll() is not None:
                    print(f"Process exited with code {p.returncode}. Terminating")
                    terminate(processes)
                    sys.exit(1)
            time.sleep(1)
    except KeyboardInterrupt:
        terminate(processes)
        sys.exit(0)
    except Exception as e:
        print(f"Exception: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()


def get_full_processes(arducam_config_path, environment):
    processes = []
    processes.append(
        subprocess.Popen(
            [
                "ros2",
                "run",
                "usb_cam",
                "usb_cam_node_exe",
                "--ros-args",
                "--remap",
                "__ns:=/usb_cam_0",
                "--params-file",
                arducam_config_path + "/rightCamera.yaml",
            ],
            env=environment,
        )
    )
    processes.append(
        subprocess.Popen(
            [
                "ros2",
                "run",
                "usb_cam",
                "usb_cam_node_exe",
                "--ros-args",
                "--remap",
                "__ns:=/usb_cam_1",
                "--params-file",
                arducam_config_path + "/leftCamera.yaml",
            ],
            env=environment,
        )
    )
    # load bearing time.sleeps
    time.sleep(5)
    processes.append(
        subprocess.Popen(
            [
                "ros2",
                "launch",
                "xsens_mti_ros2_driver",
                "xsens_mti_node.launch.py",
                "port:=/dev/xsens",
            ],
            env=environment,
        )
    )
    time.sleep(5)
    processes.append(
        subprocess.Popen(
            [
                "ros2",
                "launch",
                "rplidar_ros",
                "rplidar_s1_launch.py",
                "serial_port:=/dev/rplidar",
            ],
            env=environment,
        )
    )
    processes.append(
        subprocess.Popen(
            [
                "ros2",
                "run",
                "gps_hack",
                "gps_talker",
            ],
            env=environment,
        )
    )
    return processes

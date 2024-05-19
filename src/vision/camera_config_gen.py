from pypylon import pylon
import yaml
import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..'))
config_path = root_path + '\config\camera.yaml'
print(root_path)
print(config_path)

sys.path.insert(0, root_path)


# ToDo
# Disintegrate all functions from the __init__ method based on their implementation.

class CameraConfigurator:
    """
    CameraConfigurator class for configure cameras attached to the system.

    This class uses pypylon library to get list of all attached devices and then
    add them to the camera config file. 

    Attributes:
        max_cam_to_use (int)   :   Maximum number of cameras allowed
        tlFactory    (class)   :   Get the transport layer from pylon library
        devices      (class)   :   Fetch all attached devices
        cameras       (list)   :   List containing attached cameras
        num_cam_found  (int)   :   Number of cameras found
        cam_dict      (dict)   :   Dictionary of camera details
    """
    def __init__(self):
        # CameraConfigurator Class start point.
        print("CameraConfigurator")

        # Maximum number of cameras allowed. (Modify this if more cameras are needed)
        self.max_cam_to_use = 2

        # Get the transport layer factory.
        self.tlFactory = pylon.TlFactory.GetInstance()

        # Get all attached devices and exit application if no devices is found.
        self.devices = self.tlFactory.EnumerateDevices()
        
        if len(self.devices) == 0:
            raise pylon.RuntimeException("No camera present.")

        # Create an array of instant cameras for the found devices and avoid exceeding maxCamerasToUse.
        self.cameras = pylon.InstantCameraArray(min(len(self.devices), self.max_cam_to_use))
       
        # Fetch the number of cameras attached.
        num_cam_found = self.cameras.GetSize()

         
        # Create and attach all Pylon Devices.
        cam_dict = {}
        for itr, cam in enumerate(self.cameras):
            cam.Attach(self.tlFactory.CreateDevice(self.devices[itr]))
            # Print the model name of the camera.
            print("Using device", cam.GetDeviceInfo().GetModelName())
            cam_dict[itr+1] = [itr, cam.GetDeviceInfo().GetModelName()]

        # Create YAML file data structure
        data = {
                'max_camera': self.max_cam_to_use,
                'cameras': {
                    'measurement_camera': cam_dict[1], 
                    'nozzle_camera': cam_dict[2],
                    },

                'params': {
                    'px_mm': 3.44,
                    'width': 2048,
                    'height': 1536,
                    }
                }
    
        
        # Convert YAML data to string
        yaml_data_str = yaml.dump(data, default_flow_style=False)

        # Add comments to the YAML file
        comments = "##################################################\n" \
                   "# File: camera.yaml                              #\n" \
                   "##################################################\n\n" 

        # Combine comments and YAML data
        comment_plus_yaml_str = comments + yaml_data_str

        # Writing to a YAML file.
        with open(config_path, 'w') as file:
            file.write(comment_plus_yaml_str)

        

if __name__ == "__main__":
    cameras_info = CameraConfigurator()

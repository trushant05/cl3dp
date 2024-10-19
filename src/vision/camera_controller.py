from pypylon import pylon
import yaml
import os
import sys

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..\..'))
config_path = root_path + '\config\camera.yaml'
#print(root_path)
#print(config_path)

sys.path.insert(0, root_path)

class CameraController:
    """
    CameraController class to control camera (measurement camera).

    This class provides functions to operate pylon camera and uses
    .pfs configuration file stored in config directory.

    Attributes:
        camera_config (dict)         :   Camera configuration file parameters
        camera_name   (str)          :   Name of the camera to open ('measurement_camera)
        camera_dev_id (int)          :   Device if of the camera to access
        camera_model  (str)          :   Model of the camera to access
        pfs_path      (str)          :   Path to pfs file
        pfs_filename  (str)          :   File name of type pfs
        camera_param_filepath (str)  :   Complete path of pfs file
        tlFactory  (class)           :   Fetch instance of camera
        devices    (dict)            :   List of cameras
        camera     (class)           :   Instance of intended camera 
    """
    def __init__(self, camera_name):
         # Load camera_config.yaml file
        with open(config_path, 'r') as file:
            self.camera_config = yaml.safe_load(file)

        # Define camera with model
        self.camera_name = camera_name
        self.camera_dev_id = self.camera_config['cameras'][self.camera_name][0]
        self.camera_model = self.camera_config['cameras'][self.camera_name][1]

        # Define camera parameter filepath
        pfs_path = root_path + "\config\pfs" 
        pfs_filename = self.camera_name + ".pfs"
        self.camera_param_filepath = os.path.join(root_path, "\config\pfs", pfs_path, pfs_filename)
        #print(self.camera_param_filepath)

        # Instantiate camera
        self.tlFactory = pylon.TlFactory.GetInstance()
        self.devices = self.tlFactory.EnumerateDevices()
        self.camera = pylon.InstantCamera(self.tlFactory.CreateDevice(self.devices[self.camera_dev_id]))

        self.camera.Open()
    
    def configure_for_software_trigger(self):
        """
        Method which configures camera to work with software trigger.
        """
        self.camera.TriggerSelector.SetValue("FrameStart")
        self.camera.TriggerMode.SetValue("On")
        self.camera.TriggerSource.SetValue("Software")
    
    def start_grabbing(self):
        """
        Method which sets grabbing stragy for the camera.
        """
        self.camera.StartGrabbing(pylon.GrabStrategy_OneByOne)
    
    def stop_grabbing(self):
        """
        Method to stop grabbing of frames by camera.
        """
        self.camera.StopGrabbing()
    
    def close(self):
        """
        Method to close instance of camera.
        """
        self.camera.Close()

    def is_grabbing(self):
        """
        Method which checks if the camera is grabbing frames.
        """
        return self.camera.IsGrabbing()

    def execute_software_trigger(self):
        """
        Method which executes a software trigger.
        """
        if self.camera.WaitForFrameTriggerReady(1000, pylon.TimeoutHandling_ThrowException):
            self.camera.ExecuteSoftwareTrigger()
    
    def retrieve_result(self, timeout=5000):
        """
        Method which retrieves results from the camera.
        """
        return self.camera.RetrieveResult(timeout, pylon.TimeoutHandling_ThrowException)

if __name__ == "__main__":
    cam_ctrl = CameraController('measurement_camera')
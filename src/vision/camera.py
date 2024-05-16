import os
import sys
import yaml
import PySpin
import cv2

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, root_path)

print(root_path)

class Camera:
    """
    Camera class to capture images.

    """

    def __init__(self):
        """

        """
        
        # Retrieve singleton reference to system object
        self.system = PySpin.System.GetInstance()

        # Get current library version
        self.version = self.system.GetLibraryVersion()
        print('Library version: %d.%d.%d.%d' % (self.version.major, self.version.minor, self.version.type, self.version.build))

        # Retrieve list of camera from the system
        self.cam_list = self.system.GetCameras()


    def grab_image(self):
        image = None

        # Start acquisition
        self.camera.BeginAcquisition()

        try:
            # Capture a single image
            image_result = self.camera.GetNextImage()
            
            # Convert image to CV Mat compatible
            image = image_result.GetNDArray()


            # Ensure the image capture was successful
            if image_result.IsIncomplete():
                print('Image capture incomplete')
            else:
                # Process the image (for example, save it)
                # Note: Processing steps would go here

                # Ensure to release the image to avoid memory leaks
                image_result.Release()

        finally:
            # End acquisition
            self.camera.EndAcquisition()

            # Deinitialize the camera
            self.camera.DeInit()

            # Release system resources
            del self.camera
            self.cam_list.Clear()
            self.system.ReleaseInstance()


        return image



    def run_camera(self):

        # Assume we're using the first camera
        self.camera = self.cam_list.GetByIndex(0)
        self.camera.Init()

        # Retrieve the nodemap
        self.nodemap = self.camera.GetNodeMap()

        # Set acquisition mode to single frame
        self.acquisition_mode = PySpin.CEnumerationPtr(self.nodemap.GetNode('AcquisitionMode'))
        self.single_frame_mode = self.acquisition_mode.GetEntryByName('SingleFrame')
        self.acquisition_mode.SetIntValue(self.single_frame_mode.GetValue())



###########
            

	
if __name__ == '__main__':
    test = Camera()
    test.run_camera()
    data = test.grab_image() 
        
    # Display the image
    cv2.imshow('Example - Show image in window', data)

    # Wait for a key press and then destroy all windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()
	








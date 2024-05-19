import cv2
import sys
import os
import time

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
config_path = os.path.join(root_path, '..\config\camera.yaml')
print(root_path)
print(config_path)

sys.path.insert(0, root_path)
from vision.camera_controller import CameraController

class ImageGrabber:
    """
    ImageGrabber class which captures frame using one-by-one strategy.
    """
    def __init__(self, camera_controller):
        self.camera_controller = camera_controller
    
    def grab_image(self):
        """
        Method which grabs frames from the camera:

        Attributes:
            camera_controller    (class)   :    Instance of class which grabs frames
            grab_result          (array)   :    Grabed image in raw form
            img                  (array)   :    Grabed image in OpenCV/Numpy accessible format
        """
        # Make sure the camera is ready and start grabbing
        if not self.camera_controller.is_grabbing():
            self.camera_controller.start_grabbing()
        
        # Trigger the camera to capture an image
        self.camera_controller.execute_software_trigger()
        
        # Retrieve the captured image
        grab_result = self.camera_controller.retrieve_result()
        if grab_result.GrabSucceeded():
            # Access the image data and process it
            img = grab_result.GetArray()
        else:
            print("Failed to grab image.")
        
        grab_result.Release()
        return img

# Example usage:
if __name__ == "__main__":
    camera_controller = CameraController("measurement_camera")
    camera_controller.configure_for_software_trigger()
    
    image_grabber = ImageGrabber(camera_controller)
    
    try:
        # Grab a single image
        image = image_grabber.grab_image()
        
        cv2.imwrite('test.jpg', image)
        time.sleep(10)
            
        cv2.destroyAllWindows()
    finally:
        camera_controller.stop_grabbing()
        camera_controller.close()


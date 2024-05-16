import PySpin
import cv2

# Initialize the system and get the camera list
system = PySpin.System.GetInstance()
cam_list = system.GetCameras()

# Assume we're using the first camera
camera = cam_list.GetByIndex(0)
camera.Init()

# Retrieve the nodemap
nodemap = camera.GetNodeMap()

# Set acquisition mode to single frame
acquisition_mode = PySpin.CEnumerationPtr(nodemap.GetNode('AcquisitionMode'))
single_frame_mode = acquisition_mode.GetEntryByName('SingleFrame')
acquisition_mode.SetIntValue(single_frame_mode.GetValue())

# Start acquisition
camera.BeginAcquisition()

try:
    # Capture a single image
    image_result = camera.GetNextImage()

    image_data = image_result.GetNDArray()

    # Display the image
    cv2.imshow('Example - Show image in window', image_data)

    # Wait for a key press and then destroy all windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
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
    camera.EndAcquisition()
    
    # Deinitialize the camera
    camera.DeInit()
    
    # Release system resources
    del camera
    cam_list.Clear()
    system.ReleaseInstance()


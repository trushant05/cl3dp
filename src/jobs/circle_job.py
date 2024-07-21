class CircleJob:
    """
    A class for cprinter jobs.
    """

    def __init__(self, start, center, end, pressures, speeds):
        """
        Initializes a new instance of Job class.
        """

        # Setup Printer
        self.start = start
        self.center = center
        self.end = end
        self.pressures = pressures
        self.speeds = speeds
        #self.camera_use = camera_use
        #self.label = label
        #self.measure = measure

    def show_string(self):
        res = f"Start:{self.start}\n"
        res = f"Start:{self.center}\n"
        res = f"Start:{self.end}\n"
        #res += f"Points:{self.points}\n"
        res += f"Pressures:{self.pressures}\n"
        res += f"Speeds:{self.speeds}\n"
        #res += f"Camera Usage:{self.camera_use}\n"
        #res += f"Label:{self.label}\n"
        #res += f"Measure After:{self.measure}\n"
        return res
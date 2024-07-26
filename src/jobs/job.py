class Job:
    """
    A class for cprinter jobs.
    """

    def __init__(self, start, points, pressures, speeds, label, camera_use = True, measure=True, controlled = False):
        """
        Initializes a new instance of Job class.
        """

        # Setup Printer
        self.start = start
        self.points = points
        self.pressures = pressures
        self.speeds = speeds
        self.camera_use = camera_use
        self.label = label
        self.measure = measure
        self.controlled = controlled

    def show_string(self):
        res = f"Start:{self.start}\n"
        res += f"Points:{self.points}\n"
        res += f"Pressures:{self.pressures}\n"
        res += f"Speeds:{self.speeds}\n"
        res += f"Camera Usage:{self.camera_use}\n"
        res += f"Label:{self.label}\n"
        res += f"Measure After:{self.measure}\n"
        res += f"Controlled Iterative:{self.controlled}\n"
        return res
import socket
from time import sleep
import os
import sys
import yaml

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
config_path = os.path.join(root_path, '..\config\stages.yaml')
sys.path.insert(0, root_path)

#print(root_path)
#print(config_path)

with open(config_path, 'r') as file:
    config = yaml.safe_load(file)

# Placeholder for self.default_feedate. (do not delete)
NOTHING = object()



class Staging(object):
    """
    A base stage control class which will be inherited later.

    This class serves as the parent class for the Aerotech class and the 
    below given methods will be overwritten. Tracking of position is handled
    by this class and every time goto method is invoked it will also update
    internal state of that specific stage or stages.

    Attributes:
        substrate         (int)   :    Substrate thickness
        incremental      (bool)   :    False -> Absolute Mode, True -> Incremental Mode
        default_feedrate (float)  :    Rate of movement in each stages
        x                (float)  :    Track movement in x stage
        y                (float)  :    Track movement in y stage
        z                (float)  :    Track movement in z stage
        initilized       (bool)   :    State whether stages are initialized or not

    """

    def __init__(self, substrate = 0, incremental = False):
        """
        Initializes a new instance of Staging class.

        Parameters:
            substrate (int)     :  Substrate thickness
            incremental (bool)  :  False -> Absolute Mode, True -> Incremental Mode
        """

        self.sci = True

        self.default_feedrate = 1.0 # mm/s #Eventually replace with None
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

        #TODO
        if self.sci:
            self.b = 0.0

        self.initialized = True


    def goto(self, x = None, y = None, z = None, f = NOTHING):
        """
        Keep track of stage movement when goto is called by child class.

        Parameters:
            x (float)  :  Update movement in x stage
            y (float)  :  Update movement in y stage
            z (float)  :  Update movement in z stage
            f (float)  :  Speed of movement
        """
        print("GOTO inside Staging class")
        if f is NOTHING:
            f=self.default_feedrate
        print('Moving by', x, ' ', y, ' ', z, ' at speed ', f, ' mm/s.\n')
        if x != None:
            self.x += x
        if y != None:
            self.y += y
        if z != None:
            self.z += z

    def goto_b(self, b = None, f = NOTHING):
        if f is NOTHING:
            f=self.default_feedrate
        print('Moving by', b, ' at speed ', f, ' mm/s.\n')
        if b != None:
            self.b += b


    def gotoxyz(self, pos_array=(None,None,None), f=NOTHING):
        """
        Wrapper method over goto method for ease of logic.

        Parameters:
            pos_array (tuple)   :   Update movement in (x, y, z) stages
            f         (float)   :   Speed of movement
        """
        x=pos_array[0]
        y=pos_array[1]
        z=pos_array[2]
        self.goto(x,y,z,f)


    def goto_rapid(self, x = None, y = None, z = None):
        """
        Keep track of stage movement when goto_rapid is called by child class.
        Similar to goto method -> For high speed movement. (no feedrate parameters)

        Parameters:
            x (float)  :  Update movement in x stage
            y (float)  :  Update movement in y stage
            z (float)  :  Update movement in z stage
        """
        print('Moving rapidly by', x, ' ', y, ' ', z)
        if x != None:
            self.x += x
        if y != None:
            self.y += y
        if z != None:
            self.z += z


    def send_message(self, msg):
        """
        Method to send message to A3200 ASCII controller which is 
        implemented by child class.

        Parameters:
            msg (str)   :    Control commands
        """
        print(msg)


    def set_pos(self, x = None , y = None , z = None ): #for testing only
        """ 
        Method to set position of each stage.

        Parameters:
            x (float)    :    Position of x stage
            y (float)    :    Position of y stage
            z (float)    :    Position of z stage

        Note:
        For testing only.
        """
        if x != None:
            self.x = x
        if y != None:
            self.y = y
        if z != None:
            self.z = z


    def get_coords(self):
        """
        Method to fetch current position of each stage.

        Note:
        For testing only.
        """
        return (self.x, self,y, self,z)


    def get_pos(self, axis = None):
        """
        Method to fetch current position of given stage (axis).

        Parameters:
            axis (int)     :     0 -> x, 1 -> y, 2 -> z
        """
        if axis in ['x', 'X']:
            return float(self.x)
        elif axis in ['y', 'Y']:
            return float(self.y)
        elif axis in ['z', 'Z']: #Z fine
            return float(self.z)
        else:
            raise ValueError('staging.get_pos was called without a valid axis')



class Aerotech(Staging):
    """
    An Aerotech class which is child of Staging class with essential
    implementation in both absolute and incremental mode.

    Attributes:
        substrate         (int)   :    Substrate thickness
        incremental      (bool)   :    False -> Absolute Mode, True -> Incremental Mode
        default_feedrate (float)  :    Rate of movement in each stages 
        socket           (socket) :    Instance of socket class for communication with stages

    Example:

    Note:
        Default mode is absolute since incremental=False.


    """

    def __init__(self, substrate=0, incremental=False):
        """
        Initialize a new instance of the Aerotech class.

        Parameters:
            substrate (int)      :  Substrate thickness
            incremental (bool)  :  False -> Absolute Mode, True -> Incremental Mode

        """
        super().__init__() # Inherit variables from parent class (Staging)

        if not incremental:
            # Absolute mode
            print('Staging initialized - Absolute mode')
        if incremental:
            # Incremental mode
            print('Staging initialized - Incremental mode')


        self.default_feedrate = 1.0 # Set default feedrate

        # Setup socket communication with configuration from stages.yaml file
        self.socket = socket.socket()
        self.socket.settimeout(config['connection']['SOCKET_TIMEOUT'])
        self.socket.connect((config['connection']['PC_IP_ADDRESS'], config['connection']['PORT']))
        sleep(1)

        # Enable stages and set RAMP rate with unit system
        self.send_message('ENABLE X Y Z\n')
        if self.sci:
            self.send_message('ENABLE B\n')
        self.send_message('METRIC\n')
        self.send_message('SECOND\n')
        self.send_message('RAMP RATE 100\n')
        self.send_message('WAIT MODE INPOS\n')

        # Check the mode of stages
        if not incremental:
            # Absolute mode
            self.send_message('ABSOLUTE\n')
            self.send_message('G92 X0 Y0 Z0\n')
            print('Aerotech initialized = Absolute mode')
            self.mode = 'Absolute'

        elif incremental:
            # Incremental mode
            self.send_message('INCREMENTAL\n')
            print('Aerotech initialized = Incremental mode')
            self.mode = 'Incremental'


    def __del__(self):
        """
        This methods cleans up safety zones after object is deleted.

        """
        self.delete_safe_zones()
        print('Aerotech closed')


    def create_safe_zone(self, substrate):
        """
        Method that enables safety zones for nozzle and stages.
        
        Parameters:
            substrate (int)     :    Material on which printing takes place.

        """
        # Define Nozzle safe zone
        self.send_message('SAFEZONE 0 CLEAR\n')
        self.send_message('SAFEZONE 0 TYPE SAFEZONETYPE_NoEnter \n')
        self.send_message('SAFEZONE 0 SET X ' + repr(config['safety']['SAFE_ZONE_NOZZLE_X'][0]) + ', ' + repr(config['safety']['SAFE_ZONE_NOZZLE_X'][1]) + '\n')
        self.send_message('SAFEZONE 0 SET Y ' + repr(config['safety']['SAFE_ZONE_NOZZLE_Y'][0]) + ', ' + repr(config['safety']['SAFE_ZONE_NOZZLE_Y'][1]) + '\n')
        self.send_message('SAFEZONE 0 SET Z ' + repr(config['safety']['SAFE_ZONE_NOZZLE_Z'][substrate]) + ', ' + repr(config['safety']['SAFE_ZONE_NOZZLE_Z'][len(config['safety']['SAFE_ZONE_NOZZLE_Z']) - 1]) + '\n')
        self.send_message('SAFEZONE 0 ON\n')

        # Define AFM safe zone
        self.send_message('SAFEZONE 1 CLEAR\n')
        self.send_message('SAFEZONE 1 TYPE SAFEZONETYPE_NoEnter \n')
        self.send_message('SAFEZONE 1 SET X ' + repr(config['safety']['SAFE_ZONE_AFM_X'][0]) + ', ' + repr(config['safety']['SAFE_ZONE_NOZZLE_X'][1]) + '\n')
        self.send_message('SAFEZONE 1 SET Y ' + repr(config['safety']['SAFE_ZONE_AFM_Y'][0]) + ', ' + repr(config['safety']['SAFE_ZONE_NOZZLE_Y'][1]) + '\n')
        self.send_message('SAFEZONE 1 SET Z ' + repr(config['safety']['SAFE_ZONE_AFM_Z'][substrate]) + ', ' + repr(config['safety']['SAFE_ZONE_AFM_Z'][len(config['safety']['SAFE_ZONE_AFM_Z']) - 1]) + '\n')
        self.send_message('SAFEZONE 1 ON\n')


    def delete_safe_zones(self):
        """
        Method which deletes safezones when object is destroyed.

        """
        self.send_message('SAFEZONE 0 CLEAR\n')
        self.send_message('SAFEZONE 1 CLEAR\n')


    def get_socket(self):
        """
        Method to get socket, can be used by other classes/function
        outside Aerotech class object.

        """
        return self.socket


    def goto(self, x = None, y = None, z = None, f = NOTHING):
        """
        Method that overwrites stages.goto.
       
        Parameters:
            x (float)  :  Update movement in x stage
            y (float)  :  Update movement in y stage
            z (float)  :  Update movement in z stage
            f (float)  :  Speed of movement

        """
        print("GOTO inside Aerotech class")
        if f is NOTHING:
            f = self.default_feedrate
        if x != None or y != None or z != None:
            msg = 'LINEAR' #G1
            if x != None:
                msg += ' X' + ('%0.6f' %x)
                self.x += x
            if y != None:
                msg += ' Y' + ('%0.6f' %y)
                self.y += y
            if z != None:
                msg += ' Z' + ('%0.6f' %z)
                self.z += z
            if f != None:
                msg += ' F' + ('%0.6f' %f)

        elif f != None:
            msg = 'F' + repr(f)
        else:
            raise ValueError('staging.goto() was called with all None arguments')
        msg += '\n'
        print(msg)
        self.send_message(msg)

    def goto_b(self, b = None, f = NOTHING):

        if f is NOTHING:
            f = self.default_feedrate

        if b != None:
            msg = 'LINEAR' #G1
            if b != None:
                msg += ' B' + ('%0.6f' %b)
                self.b += b 
            if f != None:
                msg += ' F' + ('%0.6f' %f)

        elif f != None:
            msg = 'F' + repr(f)
        else:
            raise ValueError('staging.goto_b() was called with all None arguments')
        msg += '\n'
        print(msg)
        self.send_message(msg)


    def set_pressure(self, pressure = None):
        """
        Method to set pressure of the system.

        Parameters:
            pressure  (float)    :    Using the process model intended pressure is
                                      converted to respective voltage.

        Note:
            Here analog pin1 on X stage is used which might not always be the case.

        """
        if pressure != None:
            msg = '$AO[1].X = '
            msg += '%0.6f' %pressure

        else:
            raise ValueError('staging.set_pressure() was called with all None arguments')
        msg += '\n'
        print(msg)
        self.send_message(msg)


    def set_pressure_regulator(self, pressure = None):
        """
        Method to set pressure of the system.

        Parameters:
            pressure  (float)    :    Using the process model intended pressure is
                                      converted to respective voltage.

        Note:
            Here analog pin0 on X stage is used which might not always be the case.

        """
        if pressure != None:
            msg = '$DO[0].X = '
            msg += '%0.6f' %pressure

        else:
            raise ValueError('staging.set_pressure_regulator() was called with all None arguments')
        msg += '\n'
        print(msg)
        self.send_message(msg)


    def set_pressure_solenoid(self, pressure = None):
        """
        Method to set pressure of the system.

        Parameters:
            pressure  (float)    :    Using the process model intended pressure is
                                      converted to respective voltage.

        Note:
            Here analog pin6 on X stage is used which might not always be the case.

        """
        if pressure != None:
            msg = '$DO[6].X = '
            msg += '%0.6f' %pressure

        else:
            raise ValueError('staging.set_pressure_solenoid() was called with all None arguments')
        msg += '\n'
        print(msg)
        self.send_message(msg)


    def goto_xyz(self, pos_array=(None, None, None), f=NOTHING):
        """
        Method that overwrites stages.goto_xyz.

        Parameters:
            pos_array (tuple)   :   Update movement in (x, y, z) stages
            f         (float)   :   Speed of movement

        """
        x = pos_array[0]
        y = pos_array[1]
        z = pos_array[2]
        self.goto(x, y, z, f)


    def goto_rapid(self, x = None, y = None, z = None):
        """
        Method that overwrites stages.goto_rapids.
    
        Parameters:
            x (float)  :  Update movement in x stage
            y (float)  :  Update movement in y stage
            z (float)  :  Update movement in z stage 

        """
        if x != None or y != None or z != None:
            msg = 'RAPID' #G0
            if x != None:
                msg += ' X' + repr(x)
            if y != None:
                msg += ' Y' + repr(y)
            if z != None:
                msg += ' Z' + repr(z)
        else:
            raise ValueError('staging.goto_rapid() was called with all None arguments')
        msg += '\n'
        print(msg)
        self.send_message(msg)


    def send_message(self, msg):
        """
        Method that sends commands to stages via socket in the form of string.

        Parameters:
            msg (str)    :    Command to be executed by ASCII server.

        """
        print(msg)
        self.socket.send(msg.encode())
        number_of_msg = msg.count('\n')
        for msg_counter in range(number_of_msg):
            self.recv_msg = ''
            recv_str = self.socket.recv(1024).decode()
            print(recv_str)
            self.recv_msg += recv_str # builds a received message for the last command only
        if (len(self.recv_msg)>1):
            return str(self.recv_msg[1:-1])



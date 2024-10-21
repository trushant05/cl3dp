import numpy as np


def speed_ctrl_func(angles):
    """
    This function calculates some coefficients for
    Cost function in NLP_extrusion class. The speed_ctrl
    is defined based on angle between two successive points
    of printing pattern.


    :param angles: the angles between two successive point of discrete printing pattern. _type_ numpy.ndarray

    :return: a numpy ndarray of coefficients for controlling the speed magnitude term in cost function of NLP_extrusion class

    """

    speed_ctrl = np.ones((angles.shape))

    for i in range(len(angles)):
        speed_ctrl[i] = np.exp((2 * np.log(150000) / np.pi) * angles[i]) if angles[i] <= np.pi/2 else  150000

    return speed_ctrl

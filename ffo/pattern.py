import numpy as np

from src.pkg.initial_values import *

from src.pkg.utils import speed_ctrl_func

from src.pkg.pattern_params import *

##////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## *****************************************************************************************************************************
##////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

## ***** building the pattern of printing - This should be linked based on Chris pattern creation and finding the angles and then calling speed_ctrl_func(angles) *****
# reference values in dimless format
# complicated pattern

path_vector = np.linspace(0, length_of_pattern, num=Imax+1)

print(path_vector)

tau_p = 1 # in seconds


w_ref = np.full((Imax, 1), 100e-6)

w_ref[Imax//4:2*Imax//5,0] = 200e-6

w_ref[Imax//2:3*Imax//5,0] = 50e-6

s_ref = np.full((Imax, 1), 0.6e-3)


# print(s_ref)

wpr_ref = w_ref/w_max

spr_ref = (s_ref - s_min)/(s_max - s_min)

# print('wpr_ref',wpr_ref)

# print('spr_ref',spr_ref)

p_pr_expected =  ((wpr_ref * ((spr_ref+beta)**0.5))/(T1_pr))**(2*n_viscosity) -alpha

# print('p_pr_expected',p_pr_expected)

angles = np.zeros(Imax)
angles[15] = np.pi/3

angles[30] = np.pi/2-np.pi/12

angles[65] = np.pi


print(angles)

speed_ctrl = speed_ctrl_func(angles)#np.full((Imax, 1), 1)  # add a function later

print(speed_ctrl)


##////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
## *****************************************************************************************************************************
##////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
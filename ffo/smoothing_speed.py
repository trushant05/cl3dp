import numpy as np
import matplotlib.pyplot as plt
import copy as cpy
import os
import sys

# Set root path
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Join root pathr
sys.path.insert(0, root_path)


from ffo.pattern_params import *

def increasing_smooth_func(S_pr_opt_, Index, n_points, n_point_limit ,S_ed, S_b):

    n_points = min(n_points , n_point_limit-1)

    tau_sharpness = 0.1 +(n_points-6)/60

    temp_y1 = np.zeros(n_points + 1)

    for j in range(n_points+1):
        temp_y1[j]= (np.tanh((j*dx)*1000/tau_sharpness-3)*(S_ed-S_b)/2) + (S_ed + S_b)/2

    temp_y1 = temp_y1.reshape(-1, 1)

    start_index = int(Index)
    end_index = int(Index) + len(temp_y1)
    # print(temp_y1)

    # S_pr_opt_[int(Index):int(Index) + len(temp_y1)] = temp_y1
    S_pr_opt_[start_index:end_index] = np.minimum(temp_y1, S_pr_opt_[start_index:end_index])

    return(S_pr_opt_)


def decreasing_smooth_func(S_pr_opt_, Index, n_points, n_point_limit, S_ed, S_b):

    n_points = min(n_points , n_point_limit-1)

    tau_sharpness = 0.1 +(n_points-6)/60

    temp_y1 = np.zeros(n_points + 1)

    for j in range(n_points+1):
        temp_y1[j]= -(np.tanh((j*dx)*1000/tau_sharpness-3)*(S_ed-S_b)/2) + (S_ed + S_b)/2
        # print('inside decreasing for loop',S_ed,S_b)

    temp_y1 = temp_y1.reshape(-1, 1)

    start_index = int(Index)+1-len(temp_y1)
    end_index = int(Index)+1

    # print('start_index',start_index)
    # print('end_index',end_index)
    # print(temp_y1)

    S_pr_opt_[start_index:end_index] = np.minimum(temp_y1, S_pr_opt_[start_index:end_index])

    return(S_pr_opt_)

def n_points_sharpnees_func(S_ed,S_b, tau_p, s_max, s_min):
    s_avg = ( S_ed + S_b )/2
    Del_x=tau_p * (s_avg*(s_max-s_min)+s_min)
    n_points = np.floor(Del_x / dx) + 1
    n_points = int(n_points)+1

    return n_points

def plot_smooth_func(Imax, dx, S_pr_opt, S_pr_opt_smt ):
    x_end = (Imax-1)*dx
    x = np.linspace(0, x_end, Imax)

    plt.figure(figsize=(10, 6))

    plt.plot(x, S_pr_opt, 'o-',label='S_pr_opt')
    plt.plot(x, S_pr_opt_smt, 'o-', label='Smoothed Speed')
    # plt.plot(x, y2, label='1/(1+np.exp(-x))')

    # Add labels and title
    plt.xlabel('x')
    plt.ylabel('Stage Speed')
    plt.title('Smoothing function output')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()

    plt.savefig('Smoothed_speed.png', dpi=300, bbox_inches='tight')

    # Show the plot
    # plt.show()


def Speed_changes_index(S_pr_opt: np.ndarray):
    S_pr_opt_ = cpy.copy(S_pr_opt)

    indices = []
    length = len(S_pr_opt_)

    for i in range(length - 1):
        # Calculate the difference
        diff = (S_pr_opt_[i+1] - S_pr_opt_[i])/S_pr_opt_[i] # ***remember that always the velocisty should be bigger than 0. (set limitis of S not to be 0.)***

        if diff > 0.01:
            # Value increased; lower value at index i
            indices.append(i)
        elif diff < -0.01:
            # Value decreased; lower value at index i+1
            indices.append(i+1)
        else:
            # No change in value
            continue

    # Remove duplicates and sort the indices
    indices = sorted(set(indices))
    extended_indices =[0, *indices, (S_pr_opt.shape[0]-1)] # number 0 is because the first index is always important for future calculations of n_points
    n_points_limits = [ extended_indices[i+1]- extended_indices[i] for i in range(len(extended_indices)-1)]

    return indices , n_points_limits

def speed_smooth_func(S_pr_opt:np.ndarray, dx:float, angles_id:list, n_points_limits_list:list, s_max:float, s_min:float ,tau_p:float = 2):
    S_pr_opt_ = cpy.copy(S_pr_opt)

    for i in range(len(angles_id)):

        idx = angles_id[i]

        if len(n_points_limits_list) != len(angles_id) + 1:
            raise ValueError("The length of n_points_limits_list must be equal to len(angles_id) + 1.")
        else:
            n_points_limit_left = n_points_limits_list[i]
            n_points_limit_right = n_points_limits_list[i+1]

        # print(idx)

        if (S_pr_opt_[idx+1] == S_pr_opt_[idx-1]):

            # print('case 1', idx)

            S_ed = float(S_pr_opt_[idx+1][0])

            S_b = float(S_pr_opt_[idx][0])

            # print(S_ed,S_b)

            n_points = n_points_sharpnees_func(S_ed,S_b, tau_p, s_max, s_min)
            # print(n_points)

            S_pr_opt_ = increasing_smooth_func(S_pr_opt_, idx, n_points, n_points_limit_right, S_ed, S_b)

            S_pr_opt_ = decreasing_smooth_func(S_pr_opt_, idx, n_points, n_points_limit_left, S_ed, S_b)


        if (S_pr_opt_[idx+1] == S_pr_opt_[idx] and S_pr_opt_[idx-1] > S_pr_opt_[idx]):

            # print('case 2',idx)

            S_ed = float(S_pr_opt_[idx-1][0])

            S_b = float(S_pr_opt_[idx][0])

            n_points = n_points_sharpnees_func(S_ed,S_b, tau_p, s_max, s_min)

            S_pr_opt_ = decreasing_smooth_func(S_pr_opt_, idx, n_points, n_points_limit_left,S_ed, S_b)


        if (S_pr_opt_[idx-1] == S_pr_opt_[idx] and S_pr_opt_[idx+1] > S_pr_opt_[idx]):

            # print('case 3',idx)

            S_ed = float(S_pr_opt_[idx+1][0])

            S_b = float(S_pr_opt_[idx][0])

            n_points = n_points_sharpnees_func(S_ed,S_b, tau_p, s_max, s_min)

            S_pr_opt_ = increasing_smooth_func(S_pr_opt_, idx, n_points, n_points_limit_right,S_ed, S_b)


    return S_pr_opt_
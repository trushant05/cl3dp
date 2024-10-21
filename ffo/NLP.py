import casadi as ca # type: ignore
import time

import matplotlib.pyplot as plt


class NLP_extrusion:

    def __init__(self, params, wpr_ref, spr_ref, speed_ctrl, qq, ss, rr):
        self.params = params
        self.wpr_ref = wpr_ref
        self.spr_ref = spr_ref
        self.speed_ctrl = speed_ctrl
        self.qq = qq
        self.ss = ss
        self.rr = rr

    def optimize(self, params, wpr_ref, spr_ref, speed_ctrl, qq, ss, rr):

        alpha, beta , n_viscosity , T1_pr = params

        # Declare variables
        x = ca.SX.sym("x",2) #x[0]=Pressure, x[1]=Speed

        w_dummy = ((x[0]+alpha)**(1./(2*n_viscosity)) * T1_pr)/(ca.sqrt(x[1]+beta))

        # Form the NLP
        f = qq*(w_dummy - wpr_ref)**2 + ss*(x[1] - spr_ref)**2 + rr*(x[1])**2*speed_ctrl  # objective

        # Variable bounds
        lbx = [0.0001 , 0.0001]
        ubx = [1 , 1]
        # Constraints
        g = []

        # Constraint bounds
        lbg = []
        ubg = []


        nlp = {'x':x, 'f':f, 'g':ca.vertcat(*g)}

        # Pick an NLP solver
        MySolver = "ipopt"
        #MySolver = "worhp"
        #MySolver = "sqpmethod"

        # Solver options
        opts = {
            "ipopt": {
            "print_level": 0,      # Disable IPOPT output
            "sb": "yes"            # Suppress IPOPT banner
        },
        "print_time": 0            # Disable CasADi timing output
        }
        if MySolver=="sqpmethod":
            opts["qpsol"] = "qpoases"
            opts["qpsol_options"] = {"printLevel":"none"}

        # Allocate a solver
        solver = ca.nlpsol("solver", MySolver, nlp, opts)

        x_0 = [0.5 , 0.5]
        # Solve the NLP
        sol = solver(x0 = x_0, lbx=ca.vertcat(*lbx), ubx=ca.vertcat(*ubx))

        if __name__ == "__main__":
        # Print solution
            print("-----")
            print("objective at solution = ", sol["f"])
            print("primal solution = ", sol["x"])
            print("dual solution (x) = ", sol["lam_x"])
            print("dual solution (g) = ", sol["lam_g"])


        x_solution = sol["x"]

        P_pr_final = float(x_solution[0])
        S_pr_final = float(x_solution[1])

        W_pr_final = ((P_pr_final+alpha)**(1./(2*n_viscosity)) * T1_pr)/(ca.sqrt(S_pr_final+beta))

        return (P_pr_final, S_pr_final, W_pr_final)


    def plotoptimal(self, wpr_ref, spr_ref, P_pr_opt, S_pr_opt, W_pr_opt, speed_ctrl, angles, smooth_status):

        # Create a figure with 4 subplots (4 rows, 1 column)
        fig, axs = plt.subplots(5, 1, figsize=(10, 16))

        # First subplot
        axs[0].plot(wpr_ref, marker='o', label='Reference')
        axs[0].plot(W_pr_opt, marker='o', label='Optimal Solution')
        axs[0].set_xlabel('Space Index')
        axs[0].set_ylabel('Dimensionless Line Width')
        axs[0].set_title('Comparison of Dimensionless Line Width')
        axs[0].legend()
        axs[0].grid(True)
        axs[0].set_ylim(0, 0.7)  # Set y-axis limit

        # Second subplot
        axs[1].plot(spr_ref, marker='o', label='Reference')
        axs[1].plot(S_pr_opt, marker='o', label='Optimal Solution')
        axs[1].set_xlabel('Space Index')
        axs[1].set_ylabel('Dimensionless Speed')
        axs[1].set_title('Comparison of Dimensionless Stage Speed')
        axs[1].legend()
        axs[1].grid(True)
        axs[1].set_ylim(0, 0.5)  # Set y-axis limit

        # Third subplot
        axs[2].plot(P_pr_opt, marker='o', label='Optimal Solution')
        axs[2].set_xlabel('Space Index')
        axs[2].set_ylabel('Dimensionless Pressure')
        axs[2].set_title('Comparison of Dimensionless Pressure')
        axs[2].legend()
        axs[2].grid(True)
        axs[2].set_ylim(0, 1)  # Set y-axis limit

        # Fourth subplot
        axs[3].plot(1./speed_ctrl, marker='o',label='Corner Multiplier')
        axs[3].set_xlabel('Space Index')
        axs[3].set_ylabel('Speed Control Multiplier')
        axs[3].set_title('Multiplier of Sharp Angles in Cost Function')
        axs[3].legend()
        axs[3].grid(True)
        # axs[3].set_ylim(0, )  # Set y-axis limit

        axs[4].plot(angles, marker='o',label='Angle')
        axs[4].set_xlabel('Space Index')
        axs[4].set_ylabel('Angle [rad]')
        axs[4].set_title('Angle between three consequtive points')
        axs[4].legend()
        axs[4].grid(True)
        # axs[3].set_ylim(0, )  # Set y-axis limit

        # Adjust layout to prevent overlap
        plt.tight_layout()

        ##Construct the filename based on smooth_status
        if smooth_status == 'non_smooth':
            filename = 'optimal_solution_tracking_non_smooth.png'
        elif smooth_status == 'smoothed':
            filename = 'optimal_solution_tracking_smoothed.png'
        else:
            filename = f'optimal_solution_tracking_{smooth_status}.png'


        # Save the figure
        plt.savefig(filename, dpi=300, bbox_inches='tight')

        # Close the figure
        plt.close(fig)

        # Show the combined plot
        # plt.show()
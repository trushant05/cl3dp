import numpy as np
# constant parameters

k1=0.4		#the ration between H and W of printed stream. H is height, and W is the width of that. 

theta= np.pi/4   # contact angle of the line

II = (1. / (4 * np.sin(theta)**2)) * np.arccos(1 - 2*k1 * np.sin(theta))
- (1. / (2 * np.sin(theta)) - k1) * np.sqrt((k1 / np.sin(theta)) - k1**2) # constant for cross sectional area

n_viscosity=0.2297 	# power of power law model of liquid  - mu=kappa *{\dot{\gamma}}^{n-1} where \dot{\gamma} is thestrain rate with unit of 1/s and mu has unit of Pa.s.

kappa=104.56

R=76.2e-6     # the size of nozzle is 152 um.
L_nozzle=5.08e-2	#the length ## **** find a way to consider the head loss between syringe and nozzle


T1=np.sqrt( (np.pi * R**(3+(1./n_viscosity)))/((3+(1./n_viscosity))*II*(2*L_nozzle*kappa)**(1./n_viscosity)) )

psi_to_pa = 6894.76

p_max = 50 * psi_to_pa

p_min = 8 * psi_to_pa

s_max = 2e-3

s_min = 0.01e-3

w_max = (p_max**(1./(2*n_viscosity)) * T1)/(np.sqrt(s_min)) #The maximum line width is when pressure at highest value and speed at lowest value. This is just for nondimensionalizing the optimization.

alpha = p_min/(p_max-p_min)

beta = s_min/(s_max-s_min)

Tdimless = (((s_max-s_min)**0.5)* w_max)/(p_max-p_min)**(0.5/n_viscosity)

T1_pr = T1/Tdimless

constraints = (p_max, p_min, s_max, s_min, w_max )
params = (alpha, beta , n_viscosity , T1_pr)

if __name__ == "__main__":
    print('T1:',T1)
    print('Tdimless:',Tdimless)

    print('T1_pr:',T1_pr)
    print('constraints:', constraints)
    print('params:', params)
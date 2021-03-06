from scipy.integrate import odeint
from scipy.interpolate import interp1d
import numpy as np
import matplotlib.pyplot as plt
import math
from scipy.interpolate import spline


last_Q_learned = 0.0

def P_teach(t):
    return 0.8*math.sin(15.0*t)+math.cos(30.0*t)-1.4*math.sin(45.0*t)-0.5*math.cos(60.0*t)

def F(t):
    return P_teach(t)-last_Q_learned

def hopf(state, t ):

    global last_Q_learned
    print last_Q_learned

    # Oscillator index
    oscillator_index = [0, 1, 2, 3] 

    # constants
    mu = 1.0
    gamma = 8.0
    epsilon = 0.9
    eta = 0.5
    tau = 2.0

    oscillator_list = []

    omega_0 = 0.0
    theta_0 = 0.0 
    for index in oscillator_index:
    
        oscillator = {}
       
        # unpack the state vector
        oscillator['x'] = state[len(oscillator_index)*index+0]
        oscillator['y'] = state[len(oscillator_index)*index+1]
        oscillator['omega'] = state[len(oscillator_index)*index+2]
        oscillator['alpha'] = state[len(oscillator_index)*index+3]
        oscillator['phi'] = state[len(oscillator_index)*index+4]

    
        oscillator['r'] = math.sqrt((oscillator['x']*oscillator['x']) + (oscillator['y']*oscillator['y']))
        
        oscillator['theta'] = np.sign(oscillator['x'])*math.acos(-1*(oscillator['y']/oscillator['r']))
        
        # Store theta and omega for oscillator 0

        if (index==0):
            omega_0 = oscillator['omega']
            theta_0 = oscillator['theta']
        
        
        oscillator['x_d'] = (gamma*(mu - (oscillator['r']*oscillator['r']))*oscillator['x']) - (oscillator['omega']*oscillator['y']) + (epsilon*F(t)) + (tau*math.sin(oscillator['theta']-oscillator['phi']))  
        oscillator['y_d'] = (gamma*(mu - (oscillator['r']*oscillator['r']))*oscillator['y']) + (oscillator['omega']*oscillator['x'])
        oscillator['omega_d'] = -1*epsilon*F(t)*(oscillator['y']/oscillator['r'])
        oscillator['alpha_d'] = eta*oscillator['x']*F(t)
        oscillator['phi_d'] = math.sin(((oscillator['omega']/omega_0)*theta_0) - oscillator['theta'] - oscillator['phi'])
        
        oscillator_list.append(oscillator)
        
    # Calculate the learned signal
    Q_learned = 0.0
    for oscillator in oscillator_list:
        Q_learned = Q_learned + oscillator['alpha']*oscillator['x']
        
    # Track the last Q_learned
    last_Q_learned = Q_learned
        
    # Create state vector for returning
    return_state = []
    for oscillator in oscillator_list:
        return_state.append(oscillator['x_d'])
        return_state.append(oscillator['y_d'])
        return_state.append(oscillator['omega_d'])
        return_state.append(oscillator['alpha_d'])
        return_state.append(oscillator['phi_d'])
        
    return return_state
    
 
    
# Create a uniform distribution for initial omegas
omega_zeros = np.linspace(6.0,70.0,4)

# List to store initial conditions for the 4 oscillators
state0 = []

for omega_zero in omega_zeros:
    # Creating a state vector for initial conditions
    state0.append(1.0)          #x
    state0.append(0.0)          #y
    state0.append(omega_zero)   #omega
    state0.append(0.0)          #alpha
    state0.append(0.0)          #phi

print state0

t = np.arange(0.0,2.0,1)
state = odeint(hopf,state0,t)

'''    
time = np.arange(0.0,100.0,0.05)
signal = []
for t in time:
    signal.append(P_teach(t))

plt.figure()
x_sm = np.array(time)
y_sm = np.array(signal)
x_smooth = np.linspace(x_sm.min(), x_sm.max(), 100)
y_smooth = spline(time, signal, x_smooth)
plt.plot(x_smooth, y_smooth, 'red', linewidth=1)
plt.ylim([-5.0,5.0])
plt.xlabel('Time')
plt.legend(('x','P_teach'))
plt.title('Hopf oscillator equations')
plt.show()
'''



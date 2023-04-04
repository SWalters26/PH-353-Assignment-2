import numpy as np
import random
import matplotlib.pyplot as plt
import statistics as stat
#start with some x
#guess a new x' from x, can do this by multiplying by some random real number between 0,2 each time 
#apply accept/reject with probability P = min(1,e^-beta*deltaH), if accepted add x' to list, if rejected add copy of x to list and repeat from step 2 using x_copy
#delta H = x'^2 - x^2
#repeat from step 2 using x' as new x 

def prob_selector(x):
    rand = random.uniform(0,1)
    if x >= rand:
        return True
    else:
        return False
    

def function(x, N):  #input are, x = thing to be put into H=x^2, N = number of times running the program

    counter = 0
    T = 300
    k = 1
    X_values = np.zeros(N)
    H_array = np.zeros(N)
    H = x**2
    X_values[counter] = x
    H_array[counter] = H

    #np.append(X_values,x)
    #while newcounter < N:
    for i in range(N-1):
        
        x = X_values[counter]
        H = x**2
        x_trial = x*random.uniform(0.9, 1.1)
        H_trial = x_trial**2
        delta_H = H_trial - H
        
        if np.exp(-(delta_H)/(k*T)) >= 1:
            counter += 1
            X_values[counter] = x_trial
            H_array[counter] = H_trial
        else:
            if prob_selector(np.exp(-delta_H/(k*T))) == True:
                counter += 1
                X_values[counter] = x_trial
                H_array[counter] = H_trial
            else: 
                counter += 1
                X_values[counter] = x
                H_array[counter] = H    
                continue
        #markov[counter] = H
        #counter += 1
    H_mean = np.mean(H_array)
    H_uncertainty = np.sqrt((1/(N-1)))*stat.stdev(H_array)
    plt.plot(range(0,N),H_array[range(0,N)])
    plt.plot(range(0,N),X_values[range(0,N)])
    return H_mean, H_uncertainty

def plot(i,x,N):
    test_array = np.zeros((2,i))
    x_array = list(range(0,i))
    for b in range(0,i):
        test_array[:,b] = function(x,N)
    plt.plot(x_array,test_array[0])
    
    
def z(T):
    k = 1
    beta = 1/(k*T)
    return np.sqrt(np.pi/(beta))

def P(T,x,N):
    k = 1
    beta = 1/(k*T)
    return np.exp(-beta*function(x,N))/z(T)
    
def U(T):
    k = 1
    beta = 1/(k*T)
    return 1/z(T)*(np.sqrt(np.pi/(4*beta**3)))




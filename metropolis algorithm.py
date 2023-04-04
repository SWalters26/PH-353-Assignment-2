import numpy as np
import random as rand
import matplotlib.pyplot as plt
import statistics as stat
#start with some x
#guess a new x' from x, can do this by multiplying by some random real number between 0,2 each time 
#apply accept/reject with probability P = min(1,e^-beta*deltaH), if accepted add x' to list, if rejected add copy of x to list and repeat from step 2 using x_copy
#delta H = x'^2 - x^2
#repeat from step 2 using x' as new x 

def metro(x,N):
    count = 0
    k = 1
    T = 300
    beta = 1/(k*T)
    x_array = np.zeros(N+1)
    x_array[count] = x
    x_candidate = x
    while count < N:
        x_candidate = x*rand.uniform(0,2)
        delta_H = (x_array[count])**2-x_candidate**2
        if np.exp(-beta*delta_H) >= 1:
            count += 1 
            x_array[count] = x_candidate
        else:
            if x_candidate >= rand.uniform(0,1): #accept case
                count += 1
                x_array[count] = x_candidate
            else: #reject case
                x_candidate = x_array[count]
                count += 1
                x_array[count] = x_candidate
    return x_array
    

def Z(T,x,N):
    #integral of exp(-beta*H)
    # also known as the sum over number of x's of exp(-beta*x^2)
    total = 0
    k = 1
    beta = 1/(k*T)
    metro_elements = metro(x, N)
    for n in range(len(metro(x, N))):
        total += np.exp(-beta*(metro_elements[n]**2))
    return total
    
def P(T,x,N):
    k = 1
    P_array = np.zeros(N+1)
    beta = 1/(k*T)
    metro_elements = metro(x, N)
    for n in range(len(metro(x, N))):
        P_array[n] = np.exp(-beta*metro_elements[n]**2)/Z(T,x,N)
    return P_array
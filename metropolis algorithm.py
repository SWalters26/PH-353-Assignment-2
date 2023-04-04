import numpy as np
import random as rand
import matplotlib.pyplot as plt
import statistics as stat

def metro(x,N,T):
    count = 0
    k = 1
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
    #exp(-beta*H)/Z
    k = 1
    P_array = np.zeros(N+1)
    beta = 1/(k*T)
    metro_elements = metro(x, N)
    for n in range(len(metro(x, N))):
        P_array[n] = np.exp(-beta*metro_elements[n]**2)/Z(T,x,N)
    return P_array

def U(T,x,N):
    k=1
    beta = 1/(k*T)
    integral_elements = np.zeros(N)
    metro_elements = metro(x, N)
    for n in range(N):
        integral_elements[n] = (metro_elements[n]**2)*np.exp(-beta*(metro_elements[n])**2)
    U = sum(integral_elements)/Z(T,x,N)
    return U, (1/(2*beta))
    
    
def beta_plot(T,T_N,x,N):   #T = run from 0 to temp T, T_N number of T's to sample
    k = 1
    T_array = np.linspace(1,T,T_N)
    beta_array = 1/(T_array*k)
    metro_values = np.zeros((N+1,T_N))
    for n in range(1,T_N):
        metro_values[:,n] = metro(x,N,T_array[n])
    plt.plot(beta_array, metro_values[1])
    plt.xscale("log")
        
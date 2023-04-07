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
        x_candidate = x*rand.uniform(0.1,1.9)
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
    average_metro = np.mean(x_array)
    uncertainty = np.sqrt((1/(N-1)))*stat.stdev(x_array)
    return x_array,uncertainty
    

def Z(T,x,N):
    #integral of exp(-beta*H)
    # also known as the sum over number of x's of exp(-beta*x^2)
    total = 0
    k = 1
    beta = 1/(k*T)
    uncertainty = metro(x, N, T)[1]
    metro_elements = metro(x,N,T)
    for n in range(len(metro_elements)):
        total += np.exp(-beta*((metro_elements[n])**2))
    return total, uncertainty, 1/2*np.sqrt(np.pi/beta), 
    
def P(T,x,N):
    #exp(-beta*H)/Z
    k = 1
    P_array = np.zeros(N+1)
    beta = 1/(k*T)
    metro_elements = metro(x,N,T)[0]
    uncertainty = Z(T,x,N)[1]
    z = Z(T,x,N)[0]
    for n in range(len(metro(x,N,T))):
        P_array[n] = np.exp(-beta*(metro_elements[n])**2)/z
    return P_array, uncertainty

def U(T,x,N):
    k=1
    beta = 1/(k*T)
    integral_elements = np.zeros(N)
    metro_elements = metro(x,N,T)[0]
    uncertainty = Z(T,x,N)[1]
    for n in range(N):
        integral_elements[n] = (metro_elements[n]**2)*np.exp(-beta*(metro_elements[n])**2)
    U = sum(integral_elements)/Z(T,x,N)[0]
    return U, uncertainty, (1/(2*beta))
    
    
def beta_plot(T_s,T,T_N,x,N):   #T = run from T_s to temp T, T_N number of T's to sample, T_s starting temperature
    k = 1
    T_array = np.linspace(T_s,T,T_N)
    beta_array = 1/(T_array*k)
    Energy_values = np.zeros((T_N,N+1))
    for n in range(T_s,T_N):
        Energy_values[n,:] = metro(x,N,T_array[n])[0]**2
    '''
    b_s = 5 # bin size
    c_list = [c for c in range(N)]
    rolling_count = 0
    bins_array = np.zeros((T_N, N+1))
    for i in range(1,T_N):
        for c in range(N):
            for b in range(b_s):
                rolling_count += Energy_values[i,c]
                if b < b_s:
                    bin_average = rolling_count/b_s
                    bins_array[i,c] = bin_average
                    rolling_count = 0
    plt.plot(beta_array, bins_array[:,c_list]) # second element in bin array as c_list
    plt.xlabel("Inverse T (beta = 1/(k*T)")
    plt.ylabel("H(x) = x^2")
    plt.xscale("log")
    '''
    plt.plot(beta_array, Energy_values)
    plt.xlabel("Inverse T (beta = 1/(k*T)")
    plt.ylabel("H(x) = x^2")
    return Energy_values


def binning(T,T_N,x,N,b_s):
    rolling_count = 0
    bin_average = 0
    data_to_bin = metro(x,N,T)
    bin_array = np.zeros(int(N/b_s)+1)
    for c in range(N):
        for b in range(b_s):
            if c+b > N:
                break
            rolling_count += data_to_bin[c+b]
            if b < b_s:
                bin_average = rolling_count/b_s
                rolling_count = 0
                bin_array[b] = bin_average
    return bin_array


def reweight(T, T_prime, x, N):
    U_old = U(T,x,N)[0]
    metro_elements = metro(x,N,T)
    k=1
    beta = 1/(k*T)
    beta_prime = 1/(k*T_prime)
    total = 0
    total2 = 0
    for i in range(len(metro(x,N,T))):
        total += U_old * np.exp(-(beta_prime-beta)*(metro_elements[i]**2)) * np.exp(-(beta*(metro_elements[i]**2)))
    for j in range(len(metro(x,N,T))):
        total2 += np.exp(-(beta_prime-beta)*(metro_elements[i]**2)) * np.exp(-(beta*(metro_elements[i]**2)))
    U_new = total/total2
    U_new_Expected = 1/(2*beta_prime)
    U_old_Expected = 1/(2*beta)
    return U_new, U_old, U_new_Expected, U_old_Expected
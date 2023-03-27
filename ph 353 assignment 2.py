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
    markov = np.zeros(N+1)
    x_counter = np.zeros(N+1)
    counter = 0
    x_counter[counter] = x
    newcount = 0
    T = 300
    k = 1
    H = x**2
    markov[counter] = H
    counter += 1
    check_case = True
    while newcount < N:
        if check_case == True:
            x = x*random.uniform(0.9, 1.1)
        H = x**2
        delta_H = markov[counter]-H
        check_case = True
        if np.exp(-(delta_H)/(k*T)) >= 1:
            markov[counter] = H
            x_counter[counter] = x
            counter += 1
            newcount +=1
        else:
            if prob_selector(np.exp(-delta_H/(k*T))) == True:
                markov[counter] = H
                x_counter[counter] = x
                counter += 1
                newcount +=1
            else: 
                x = x_counter[counter]
                counter += 1
                x_counter[counter] = x
                newcount +=1
    average = np.mean(markov)
    uncertainty = np.sqrt((1/(N-1)))*stat.stdev(markov)
    plt.plot(range(0,N),markov[range(0,N)])
    return average, uncertainty


def plot(x,N,i):
    test = np.zeros((2,i))
    plot_x = list(range(0,i))
    for n in range(0,i):
        test[:,n] = function(x,N)
    plt.errorbar(plot_x,test[0], yerr = test[1], ecolor='r')
        
    
    
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

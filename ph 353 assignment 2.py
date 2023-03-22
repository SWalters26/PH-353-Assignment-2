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
    markov = np.zeros(N)
    counter = 0
    #newcounter = 0
    T = 300
    k = 1.38*(10**-23)
    H = x**2
    markov[counter] = H
    counter += 1
    x_new = x
    check_case = True
    #while newcounter < N:
    for i in range(N-1):
        if check_case == True:
            x_new = x_new*random.uniform(0, 2)
        H = x_new**2
        delta_H = markov[counter-1]-H
        check_case = True
        if np.exp(-(delta_H)/(k*T)) >= 1:
            markov[counter] = H
            counter += 1
            #newcounter += 1 
        else:
            if prob_selector(np.exp(-delta_H/(k*T))) == True:
                markov[counter] = H
                counter += 1
                #newcounter += 1
            else: 
                check_case = False
                continue
        #markov[counter] = H
        #counter += 1
    average_markov = np.mean(markov)
    uncertainty = np.sqrt((1/(N-1)))*stat.stdev(markov)
    return average_markov, uncertainty


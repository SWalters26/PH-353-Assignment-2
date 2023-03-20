import numpy as np
import random
#start with some x
#guess a new x' from x, can do this by multiplying by some random real number between 0,2 each time 
#apply accept/reject with probability P = min(1,e^-beta*deltaH), if accepted add x' to list, if rejected add copy of x to list and repeat from step 2 using x_copy
#delta H = x'^2 - x^2
#repeat from step 2 using x' as new x 


def H_squared(x):
    H=x**2
    return H

def function(x, N):  #input are, x = thing to be put into H=x^2, N = number of times running the program
    markov = np.zeros(N+1)
    counter = 0
    H = x**2
    markov[counter] = H
    counter += 1
    for i in range(N):
        x_new = x*random.uniform(0, 2)
        H = H_squared(x_new)
        markov[counter] = H
        counter += 1
    return markov
    
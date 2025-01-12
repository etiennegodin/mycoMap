import numpy as np
import matplotlib.pyplot as plt

def f(x):
    
    value = -8.73214286 + 0.30357143 * x
    return value 


x = np.linspace(35,100)

y = f(x)

plt.plot(x, y)
plt.show()
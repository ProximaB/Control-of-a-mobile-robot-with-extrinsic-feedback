import matplotlib.pyplot as plt
import numpy as np


def sinus2d(x, y):
    return np.sin(x) + np.sin(y)


xx, yy = np.meshgrid(np.linspace(0, 2*np.pi, 100), 
                     np.linspace(0, 2*np.pi, 100))
z = sinus2d(xx, yy)  # Create the image on this grid

plt.imshow(z, origin = 'lower', interpolation = 'none')
plt.show()

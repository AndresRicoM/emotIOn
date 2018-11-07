import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

a = np.loadtxt(open("AndresRico_Acumulado1.csv", "rb"), delimiter = ",", skiprows = 1) #Take Data from file on src path

X = a[:,0:6]
Y = a[:,10]

xlabels = ['X Acceleration', 'Y Acceleration', 'Z Acceleration', 'Temperature', 'Light', 'Humidity']

plt.style.use('dark_background')

counter = 1

for fig in range(0,6):
    for aux in range(0,6):
        if fig == aux:
            print 'Equal'
        else:
            plt.figure(counter)
            plt.plot(X[:,fig],X[:,aux],'o')
            plt.title(xlabels[fig] + ' with respect to ' + xlabels[aux])
            plt.xlabel(xlabels[fig])
            plt.ylabel(xlabels[aux])
            counter = counter + 1

for fig in range(0,5):
    plt.figure(counter)
    plt.plot(X[:,fig], Y, 'o')
    plt.title(xlabels[fig] + ' with respect to Emotional States')
    plt.ylabel('Class')
    plt.xlabel(xlabels[fig])
    counter = counter + 1



plt.show()

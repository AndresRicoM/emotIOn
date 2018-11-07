import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

a = np.loadtxt(open("AndresRico_Acumulado1.csv", "rb"), delimiter = ",", skiprows = 1) #Take Data from file on src path

a[np.lexsort(a[:, 10])]

print a

X = a[:,0:6]
Y = a[:,10]

x = [1, 2, 3, 4, 5]
y = [1, 2, 3, 4, 5]
z = [1, 2, 3, 4, 5]

xlabels = ['X Acceleration', 'Y Acceleration', 'Z Acceleration', 'Temperature', 'Light', 'Humidity']

plt.style.use('dark_background')

counter = 0

fig = plt.figure(1)
ax = fig.add_subplot(111, projection = '3d')
ax.scatter(x,y,4, c='m')
ax.scatter(x,y,3, c='b')
ax.scatter(x,y,2, c= 'y')
ax.scatter(x,y,1, c='r')




'''
for figs in range(0,6):
    for aux in range(0,6):
        if figs == aux:
            print 'Hi'
        else:
            fig = plt.figure(counter)
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(X[:,figs], X[:,aux], Y,'o')
            ax.set_xlabel(xlabels[figs])
            ax.set_ylabel(xlabels[aux])
            ax.set_zlabel('Emotional State')
            counter = counter + 1
'''

plt.show()

import numpy as np

a = np.loadtxt(open("AndresRico_Sabado13Oct.csv", "rb"), delimiter = ",", skiprows = 1)

Y = a[:,10]
X = a[:,0:9]

for times in range(9):
    X[:,times] = X[:,times]/np.amax(X[:,times])

Y = Y / np.amax(Y)

print Y
print X

import numpy as np
import random

X = np.zeros((20000,5))
Xtest = np.zeros((6000,5))
Y = np.zeros((20000,1))
Ytest = np.zeros((6000,1))

for row in range(20000):
    for col in range (5):
        X[row, col] = random.random()

for row in range(6000):
    for col in range (5):
        Xtest[row, col] = random.random()

for row in range(20000):
    for col in range(1):
        Y[row, col] = random.randint(0,3)

for row in range(6000):
    Y[row, 0] = random.randint(0,3)

print X
print Y

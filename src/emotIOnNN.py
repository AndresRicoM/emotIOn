import tensorflow as tf                                                         #Import needed libraries
from tensorflow import keras                                                    #Machine learning
import numpy as np                                                              #Array handling
import matplotlib.pyplot as plt                                                 #Plotting
import socket
import time
import re

UDP_IP = "192.168.0.23" #Specify IP Address
UDP_PORT = 19990 #Specify UDP Communication property

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

a = np.loadtxt(open("AndresRico_Acumulado1.csv", "rb"), delimiter = ",", skiprows = 1) #Take Data from file on src path

for i in range(50): #Shuffle Data 50 times
    np.random.shuffle(a)

index = int(round(a.shape[0] * .8)) #Divide data into test (20%) set and training set (80%)

Y = a[0:index,10] #Create X, Y, Xtest and Ytest arrays
Y = Y - 1
X = a[0:index,0:6]
Xtest = a[(index + 1):a.shape[0],0:6]
Ytest = a[(index + 1):a.shape[0],10]
Ytest = Ytest - 1

class_names = ['Anger', 'Joy', 'Sadness', 'Disgust'] #Class names for identification

model = keras.Sequential([ #Create Keras sequential model with input layer of 6 and two hidden layers of 200 neurons.

    keras.layers.Dense(200,input_dim = 6 , activation = 'relu'),
    keras.layers.Dense(200, activation=tf.nn.relu, use_bias=True, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None),
    keras.layers.Dense(200, activation=tf.nn.relu, use_bias=True, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None),
    #Output layer for predictions (Softmax classification)
    keras.layers.Dense(4, activation=tf.nn.softmax, use_bias=True, kernel_initializer='glorot_uniform', bias_initializer='zeros', kernel_regularizer=None, bias_regularizer=None, activity_regularizer=None, kernel_constraint=None, bias_constraint=None)

])

model.compile(optimizer='rmsprop', #Compile model
              loss='sparse_categorical_crossentropy', # mean_squared_error / sparse_
              metrics=['accuracy'])

history = model.fit(X, Y, batch_size = 500, epochs=60) #Train model with a batch size of 500 and 60 epochs.

test_loss, test_acc = model.evaluate(Xtest, Ytest) #Evaluate model with test set

print('Test accuracy:', test_acc)

predictions = model.predict(Xtest) #Make predictions.

model.summary() #Print model summary on console.
model.get_config()

plt.style.use('dark_background') #Set dark background to plots.

plt.figure(1)
plt.plot(history.history['acc']) #Plot Accuracy Curve
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['train'], loc='upper left')

plt.figure(2)
plt.plot(history.history['loss']) #Plot Loss Curvecompletedata = []
plt.title('Model Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['train'], loc='upper left')

plt.figure(3) #Plots first 50 examples of test set. If prediction is correc it will have a green dot, if wrong it will have a red cross.
for times in range(100):
    if np.argmax(predictions[times]) == Y[times]:
        plt.plot(times, (Y[times]), 'go')
    else:
        plt.plot(times, np.argmax(predictions[times]), 'rx')
        #plt.plot(times, ((Y[times])), 'bo')
    plt.axis([0, 50, -1, 4])
    plt.title('Prediction Space')
    #plt.legend()
plt.show()

#Live predictions when streming terMITe data to computer that runs this program.
while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    indata = np.fromstring(data, dtype = float, sep = ',')
    indata = indata[0:5]
    indata = np.expand_dims(indata, 0)
    prediction = model.predict(indata)
    print class_names[np.argmax(prediction[0])]
    time.sleep(60) #Predicts emotion every minute.

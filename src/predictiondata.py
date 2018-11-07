import socket
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib import colors

#######MODIFY THE FOLLOWING TWO LINES ##########################################################
UDP_IP = "192.168.0.23" #Use the same address that was specified on the UDP Settings.
UDP_PORT = 19990 #Use the same port that was specified on the UDP Settings.
################################################################################################

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))

completedata = [[0,0,0,0,0,0],[0,0,0,0,0,0]]
counter = 0
countmat = []

while counter < 60:
    counter = counter + 1
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    indata = np.fromstring(data, dtype = float, sep = ',')
    indata = indata[0:6]
    if counter == 2:
        completedata = completedata[2:,:]
    completedata = np.vstack([completedata, indata])
    countmat = np.append(countmat, counter)
    print completedata
    time.sleep(1)

x = completedata[:,0]
y = completedata[:,1]
z = completedata[:,2]
temp = completedata[:,3]
light = completedata[:,4]
humidity = completedata[:,5]
#completedata = []

plt.plot(countmat,x,'r-', label = 'X')
plt.plot(countmat,y,'b-', label = 'Y')
plt.plot(countmat,z,'g-', label = 'Z')
plt.plot(countmat,temp,'y-', label = 'Temperature')
plt.plot(countmat,light,'k-', label = 'Light')
plt.plot(countmat, humidity,'m-', label = 'Humidity')
plt.legend(['X','Y','Z','Temperature','Light','Humidity'], loc='lower left')
#plt.plot([1,2,3], [1,2,3], 'go-', label='line 1', linewidth=2)
plt.axis([0, 61, -20, np.max(completedata) + 20 ])
plt.show()

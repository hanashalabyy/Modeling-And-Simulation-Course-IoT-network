import random
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

#r in meter , time in ms
#power transmitted = 14-30 = -16 dB


users= [0]*110
successfulTransmission=[0]*110
a=0
for k in range(100, 1200, 10):    
    users[a]=k    
    powerR = [0]*k
    fr = [0]*k
    packets = [0]*k 
    x_sigma = [0]*k
    pathloss = [0]*k
    mean_p = [0]*k
    std_dev_p = [0]*k
    x= [0]*k
    inter_arrivaltime = [0]*k
    arrivaltime = [0]*k
    # rmin = 0.1 (10*3)
    # rmax = 1 (10*3)

    collision = [0]*k #drop of packet
    count = 0
    correctdec= [0]*k

    for i in range (k):  
        fr[i] = random.random()
        packets[i] = 0.9*(math.sqrt(fr[i])) + 0.1 
        x_sigma[i] = random.gauss(0,8)
        # x_sigma[i] = np.random.normal(0,8)
        pathloss[i] = 128.1 + 37.6*math.log(packets[i],10) + x_sigma[i]
        powerR[i] = (-16 - pathloss[i]) + 30
        inter_arrivaltime[i] = np.random.exponential(10000*60)

    mean_p = np.mean(powerR)
    std_dev_p = np.std(powerR)
    x = np.linspace(np.min(powerR), np.max(powerR), 100)
    pdf = norm.pdf(x, loc=mean_p, scale=std_dev_p)
    
    if(k>990 and k<=1000):
        plt.plot(x, pdf)
        plt.xlabel('Received Power in dBm')
        plt.ylabel('Probability Density')
        plt.title('PDF of Received Power')
        plt.grid()
        plt.show()

    arrivaltime[0] = inter_arrivaltime[0]
    for j in range (0,k-2):
        for n in range(j+1,k-1):
            if((collision[j]!=1) & (collision[n]!=1)):
                
                if(abs(inter_arrivaltime[j] - inter_arrivaltime[n]) >= 62):
                   collision[j] = 0
                   collision[n] = 0
                else:
                   if(abs(powerR[j] - powerR[n]) > 36):            #power unit dBm ,  Signal to Interference ratio = 6 + 30 = 36 dB
                        if(powerR[j]>=powerR[n]):
                            collision[n]=1
                        else:
                            collision[j]=1
                   else:
                        collision[j]=1
                        collision[n]=1
        #if collision[j] == 0:
        #    count += 1
        #correctdec[j] = (count / (j+1)) * 100
    count=0
    for q in range (k):
        if collision[q]==0:
            count+= 1
    successfulTransmission[a]= (count/k) *100        
    a+=1
    
    #print(collision)
    #print(correctdec)
    #print(range(k))
    #print(correctdec)

print(users)
print(successfulTransmission)
plt.figure()
plt.plot(users, successfulTransmission)
plt.xlabel('Number of Users')
plt.ylabel('Percentage of Successfully Decoded Packets')
plt.title('Successfully Decoded Packets vs Number of Users')
plt.grid()
plt.show()

    # print(users)
    # print(pathloss)
    # print(powerR)
    # print(count)
    # print(collision)
    # print(correctdec)
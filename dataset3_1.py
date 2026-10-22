import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

fq=[]
I=[]
with open("dataset3.txt","r") as f:
    f=f.read()
    fp=f.split()
    for i in range(0,len(fp),2):
        fq.append(float(fp[i]))
        I.append(float(fp[i+1]))
    fq = np.array(fq)
    I  = np.array(I)

h = 6.626e-34
k = 1.38e-23  
c = 3e8

def black_body(fq,T):
    return (2 * h * (fq**3) / (c**2)) / (np.exp((h * fq) / (k * T)) - 1)

(T),_= curve_fit(black_body, fq, I, p0=300)
print(f"The estimated temperature is approximately {T} K")

plt.plot(fq, I, label='Simulated Data')
plt.plot(fq, black_body(fq, T), label='Estimated Curve')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Intensity')
plt.title('Black Body Radiation Curve')
plt.legend()
#plt.show()
plt.savefig("data3pic_1.png")
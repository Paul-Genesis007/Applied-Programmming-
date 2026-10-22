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


def black_body(fq,T,h,k,c):
    return (2 * h * (fq**3) / (c**2)) / (np.exp((h * fq) / (k * T)) - 1)

(T,h,k,c),_= curve_fit(black_body, fq, I, p0=(4549,6.45e-34,1.3e-23,2.45e8))
print(f" The estimated temperature is approximately {T} K,\n The estimated Plank's constant is {h} Js,\n The estimated Blotzmann'sconstant is {k} \n The estimated speed of light is {c} m/s\n")

plt.plot(fq, I,'g' ,label='Simulated Data')
plt.plot(fq, black_body(fq,T,h,k,c),'r' ,label='Estimated Curve')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Intensity')
plt.title('Black Body Radiation Curve')
plt.legend()
#plt.show()
plt.savefig("data3pic_2.png")
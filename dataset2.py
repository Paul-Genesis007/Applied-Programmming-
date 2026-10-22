import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
x=[]
y=[]

with open("dataset2.txt","r") as f:
    f=f.read()
    fp=f.split()
    for i in range(0,len(fp),2):
        x.append(float(fp[i]))
        y.append(float(fp[i+1]))
    x=np.array(x)    
    y=np.array(y)

#plt.plot(x,y)
#plt.show()
#From plot we know the highest timeperiod i.e T=2.5007
def f1(x, w, p0, p1, p2):
    return p0 * np.sin(x*w) + p1 * np.sin(3*w*x) + p2 * np.sin(5*w*x)

w=(2*np.pi)/2.5007

M = np.column_stack([np.sin(x*w), np.sin(3*w*x), np.sin(5*w*x)])
(p0,p1,p2),_,_,_= np.linalg.lstsq(M, y, rcond=None)
print(f"The estimated parameters are: {p0} sin({w}(x)) + {p1} sin({w*3}(x)) + {p2} sin({w*5}(x))")
yest=f1(x,w,p0,p1,p2)

(w1, p_0, p_1, p_2), _ = optimize.curve_fit(f1, x, y, p0=(2,5,1,1))
ycurfit=f1(x,w1,p_0, p_1, p_2)
print(f"The estimated parameters by curvefit are: {p_0} sin({w1}(x)) + {p_1} sin({w1*3}(x)) + {p_2} sin({w1*5}(x))")

plt.plot(x,y,label="Given curve")
plt.plot(x,yest,label="Estimated curve")
plt.title('Sine Curve Using lstsq')
plt.legend()
#plt.show()
plt.savefig("data2pic_1.png")
plt.cla()           #clears memory in plots

plt.plot(x,y,'g',label="Given curve")
plt.plot(x,ycurfit,'r',label="Curvefit curve")
plt.title('Sine Curve Using Curvefit')
plt.legend()
#plt.show()
plt.savefig("data2pic_2.png")
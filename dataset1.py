import numpy as np
import matplotlib.pyplot as plt

t=[]
g=[]
with open("dataset1.txt","r") as f:
    f=f.read()
    fp=f.split()
    for i in range(0,len(fp),2):
        t.append(float(fp[i]))          #Storing data from the first column in dataset1.txt
        g.append(float(fp[i+1]))        #Storing data from the second column in dataset1.txt
    t=np.array(t)
    g=np.array(g)

def stline(x, m, c):
    return m*x +c

M = np.column_stack([t, np.ones(len(t))])
(p1, p2), _, _, _ = np.linalg.lstsq(M, g, rcond=None)
print(f"The estimated equation is {p1} t + {p2}")

yest = stline(t, p1, p2)
plt.plot( t, g,color='orange',label="Given curve")
plt.plot( t, yest,'g',label="Estimated curve")
plt.errorbar(t[::25], g[::25], yerr=np.std(yest)/4, fmt='ro',label="ERROR BAR")
plt.xlabel('X')
plt.ylabel('Y')
plt.legend()
#plt.show()
plt.savefig("data1pic.png")
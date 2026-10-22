import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize
import csv

with open("Admission_Predict_Ver1.1.csv") as f:
    d=csv.reader(f)
    d=list(d)
    data=[]
    lists=[]
    for i in range (1,9):       # This two for loops are for storing the data in order without considering the first line.
        for r in range(1,501):
            data.append(float(d[r][i]))
    for i in range(0, len(data), 500): # This for loop is for grouping the data into correct list os lists.
        group = data[i:i+500]
        lists.append(group)
    for i in range(8):      # This for loop is for making lists into np array.
        lists[i]=np.array(lists[i])

def f3(lists,a,b,c,d,e,f,g,e3):  # The linear function I considered.
    return a*(lists[0])+b*(lists[1])+c*(lists[2])+d*(lists[3])+e*(lists[4])+f*(lists[5])+g*lists[6]+e3

(a1,b1,c1,d1,e1,f2,g1,e3), _ = optimize.curve_fit(f3,lists,lists[7],p0=(0,1,0.3,0.5,0.5,0.5,0.5,1))
print(f"COA={a1}(GRE)+{b1}(TOEFL)+{c1}(Rating)+{d1}(SOP)+{e1}(LOR)+{f2}(CGPA)+{g1}(Research)+{e3}")
ycurfit=f3(lists,a1,b1,c1,d1,e1,f2,g1,e3)
t=np.mean(abs(ycurfit-lists[7])/lists[7])   # Finding the error the obtained values and given COA.
print(f"The fraction of Error between the obtained value and give value of chance of admit is {t} ")
import numpy as np
from numpy import cos, sin, pi, exp 
import matplotlib.pyplot as plt
from matplotlib import cm
import mpl_toolkits.mplot3d.axes3d as plot3d
plt.style.use('_mpl-gallery-nogrid')
from matplotlib.animation import FuncAnimation

#------------------------------------->>>>1D Functions(f1 and f5)<<<<-----------------------------------------------#

# Function for gradient descent optimization on a univariate function
def grad_desc_1(f, df, s,point):
    # Initialize starting point
    a=s[0]
    b=s[1]
    xbase = np.linspace(a, b, 1000)
    ybase = f(xbase)
    bestx = point
    fig, ax = plt.subplots()
    ax.plot(xbase, ybase)
    xall, yall = [], []
    lnall,  = ax.plot([], [], 'ro')
    lngood, = ax.plot([], [], 'go', markersize=10)

    # Learning rate 
    lr = 0.01
    def onestepderiv(frame):
        nonlocal bestx, lr
        x = bestx - df(bestx) * lr 
        bestx = x
        y = f(x)
        lngood.set_data(x, y)
        xall.append(x)
        yall.append(y)
        lnall.set_data(xall, yall)

    ani= FuncAnimation(fig, onestepderiv, frames=range(1000), interval=10, repeat=False) #For showing the plot  
    plt.show()

# Define a univariate function and its derivative
def f1(x):
    return x ** 2 + 3 * x + 8

def df1(x):
    return 2 * x + 3
grad_desc_1(f1, df1, [-5,5],2)

# Define a univariate function and its derivative
def f5(x):
    return np.cos(x)**4 - np.sin(x)**3 - 4*np.sin(x)**2 + np.cos(x) + 1

def df5(x):
    return (-1*np.sin(x))*(4*np.cos(x)**3+3*np.sin(x)*np.cos(x)+8*np.cos(x)+1)
grad_desc_1(f5, df5,[0,2*np.pi],3 )

#------------------------------------->>>>2D Function(f3)<<<<-----------------------------------------------#


# Function for gradient descent optimization on a bivariate function
def grad_desc(f, a, *args):
    n=len(args)
    x=[]
    df=[]

    for i in range(0,int(n/2)):
        x.append(float(args[i]))
    for i in range(int(n/2),n):
        df.append(args[i])
    temp=[0 for i in range(len(x))]
    
    for j in range(200000):
        for i in range(len(x)):
            temp[i]=x[i]
            temp[i] = temp[i] - df[i](*x) * a 
        for i in range(len(x)):
            x[i]=temp[i]
    return x, f(*x)

# Define a bivariate function f3 and its partial derivatives
def f3(x, y):
    return x**4 - 16*x**3 + 96*x**2 - 256*x + y**2 - 4*y + 262

def df3_dx(x, y):
    return 4*x**3 - 48*x**2 + 192*x - 256
def df3_dy(x, y):
    return 2*y - 4

# Perform gradient descent on f3
print(f'The minimum of the function f3 is {grad_desc(f3, 0.05, 5, 5, df3_dx, df3_dy )}')

# Create a meshgrid for 3D plotting
xbase1 = np.linspace(-10, 10, 100)
ybase1 = np.linspace(-10, 10, 100)
xmesh1, ymesh1 = np.meshgrid(xbase1, ybase1)
zmesh1 = f3(xmesh1, ymesh1)
bestx1, besty1 = -1,-1
 
lr1 = 0.001

# Create a 3D plot for f3
fig1 = plt.figure()
ax1 = plot3d.Axes3D(fig1, auto_add_to_figure=False)
fig1.add_axes(ax1)
ax1.plot_surface(xmesh1, ymesh1, zmesh1)

# Initialize lists for storing points in the optimization process
xall1, yall1, zall1 = [], [], []
lnall1,  = ax1.plot([], [], [], 'ro')
lngood1, = ax1.plot([], [], [], 'go',markersize=10)
xall1.append(bestx1)
yall1.append(besty1)
zall1.append(f3(bestx1, besty1))

# Function for one step of gradient descent optimization
def onestepderiv1(frame):
    global bestx1, besty1, lr1
    x = bestx1 - df3_dx(bestx1, besty1) * lr1
    y = besty1 - df3_dy(bestx1, besty1) * lr1
    bestx1, besty1 = x, y
    z = f3(x, y)
    lngood1.set_data([x], [y])
    lngood1.set_3d_properties([z])
    xall1.append(x)
    yall1.append(y)
    zall1.append(z)
    lnall1.set_data(xall1, yall1)
    lnall1.set_3d_properties(zall1)

# Create animation for the optimization process
ani = FuncAnimation(fig1, onestepderiv1, frames=range(1000), interval=10, repeat=False)
plt.show()

#------------------------------------->>>>2D Function(f4)<<<<-----------------------------------------------#


# Define another bivariate function f4 and its partial derivatives
def f4(x,y):
    return exp(-(x - y)**2)*sin(y)

def df4_dx(x, y):
    return -2*exp(-(x - y)**2)*sin(y)*(x - y)

def df4_dy(x, y):
    return exp(-(x - y)**2)*cos(y) + 2*np.exp(-(x - y)**2)*sin(y)*(x - y)

# Perform gradient descent on f4
print(f'The minimum of the fuction f4 is {grad_desc(f4, 0.01, -0.1, -0.1, df4_dx, df4_dy)}')

# Create a meshgrid for 3D plotting
xbase2 = np.linspace(-pi, pi, 100)
ybase2 = np.linspace(-pi, pi, 100)
xmesh2, ymesh2 = np.meshgrid(xbase2, ybase2)
zmesh2 = f4(xmesh2, ymesh2)
bestx2, besty2 = -1,0
 
lr2 = 0.05

# Create a 3D plot for f4
fig2 = plt.figure()
ax2 = plot3d.Axes3D(fig2, auto_add_to_figure=False)
fig2.add_axes(ax2)
ax2.plot_surface(xmesh2, ymesh2, zmesh2)

# Initialize lists for storing points in the optimization process
xall2, yall2, zall2 = [], [], []
lnall2,  = ax2.plot([], [], [], 'ro')
lngood2, = ax2.plot([], [], [], 'go',markersize=10)

# Function for one step of gradient descent optimization
def onestepderiv2(frame):
    global bestx2, besty2, lr2
    x = bestx2 - df4_dx(bestx2, besty2) * lr2
    y = besty2 - df4_dy(bestx2, besty2) * lr2
    bestx2, besty2 = x, y
    z = f4(x, y)
    lngood2.set_data([x], [y])
    lngood2.set_3d_properties([z])
    xall2.append(x)
    yall2.append(y)
    zall2.append(z)
    lnall2.set_data(xall2, yall2)
    lnall2.set_3d_properties(zall2)

# Create animation for the optimization process
ani = FuncAnimation(fig2, onestepderiv2, frames=range(1000), interval=10, repeat=False)
plt.show()
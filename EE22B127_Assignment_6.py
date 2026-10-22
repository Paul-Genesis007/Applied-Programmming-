import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import random

# Read data from file
filename = "tsp40.txt"
with open(filename, "r") as file:
    data = file.readlines()
    n = int(data[0])
    x = []
    y = []
    for i in range(1, n+1):
        l = data[i].split()
        x.append(float(l[0]))
        y.append(float(l[1]))

# Create a list of city coordinates
cities = []
for i in range(len(x)):
    cities.append([x[i], y[i]])
cities = np.array(cities)

def tsp(cities):
    n = len(cities)
    bestdist1 = 0
    cityorder = [0]

    # Initialize the city order to be the sequential order
    cityorder += list(range(1, n))
    bestdist1 += sum(((cities[cityorder[i]][0] - cities[cityorder[i-1]][0])**2 + (cities[cityorder[i]][1] - cities[cityorder[i-1]][1])**2)**0.5 for i in range(1, n))
    bestdist1 += ((cities[cityorder[n-1]][0] - cities[cityorder[0]][0])**2 + (cities[cityorder[n-1]][1] - cities[cityorder[0]][1])**2)**0.5

    T = 40.0
    decayrate = 0.95

    # Simulated Annealing Loop
    for _ in range(10000):
        dist = 0
        order = cityorder[:]
        l = random.sample(range(1, n-1), 2)
        r = l[0]
        p = l[1]
        order[r], order[p] = order[p], order[r]

        # Calculate the new distance
        for i in range(1, n):
            dist += ((cities[order[i]][0] - cities[order[i-1]][0])**2 +(cities[order[i]][1] - cities[order[i-1]][1])**2)**0.5
        dist += ((cities[order[n-1]][0] - cities[order[0]][0])**2 +(cities[order[n-1]][1] - cities[order[0]][1])**2)**0.5

        if dist < bestdist1:  # If the new solution is better, accept it
            bestdist1 = dist
            cityorder = order[:]
        else:
            toss = np.random.random_sample()
            if toss < np.exp(-(dist - bestdist1) / T):  # Accept worse solution with some probability
                bestdist1 = dist
                cityorder = order[:]

        T = T * decayrate  # Reduce temperature

    return cityorder

def distance(cities, cityorder):    # Calculating total distance using Euclidean Distance Formula.
    totaldistance = 0
    n = len(cityorder)

    for i in range(1, n):
        totaldistance += ((cities[cityorder[i]][0] - cities[cityorder[i-1]][0])**2 +(cities[cityorder[i]][1] - cities[cityorder[i-1]][1])**2)**0.5
    totaldistance += ((cities[cityorder[n-1]][0] - cities[cityorder[0]][0])**2 +(cities[cityorder[n-1]][1] - cities[cityorder[0]][1])**2)**0.5
    return totaldistance

# Find an optimal city order using the tsp function
cityorder1 = tsp(cities)

# Print the optimal city order and its distance
print(cityorder1)
print(distance(cities, cityorder1))

# Prepare data for plotting
x_cities = np.array(x)
y_cities = np.array(y)
xplot = x_cities[cityorder1] 
yplot = y_cities[cityorder1]
xplot = np.append(xplot, xplot[0])
yplot = np.append(yplot, yplot[0])

# Plot the tour
plt.plot(xplot, yplot, 'o-')
plt.show()
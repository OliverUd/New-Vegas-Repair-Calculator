from mayavi import mlab as m
import numpy as n

def initialise(items):
    x = n.linspace(0, 1, 101)
    y = n.linspace(0, 1, 101)
    added = n.zeros((101, 101))
    repaired = n.zeros((101, 101))
    difference = n.zeros((101, 101))
    highVal = n.max([items[0], items[1]])
    return x, y, added, repaired, difference, highVal

def generate(items, added, repaired, difference, highVal):
    for xVal in range(101):
        for yVal in range(101):
            added[xVal][yVal] = x[xVal] ** 1.5 * items[0] + y[yVal] ** 1.5 * items[1]
            high, low = (x[xVal], y[yVal]) if x[xVal] > y[yVal] else (y[yVal], x[xVal])
            repaired[xVal][yVal] = (n.min([(0.05 + (0.15 * (skill / 100)) +
            high + (low * 0.05)), 1]) ** 1.5) * highVal
            difference[xVal][yVal] = repaired[xVal][yVal] - added[xVal][yVal]

def compareGraph(items, added, repaired):
    size = items[0] + items[1]
    extents = [0, size, 0, size, repaired[0][0], repaired[100][100]]
    m.surf(repaired, extent=extents, color=(0.2, 0.4, 1))
    extents[4], extents[5] = 0, size
    m.surf(x, y, added, extent=extents, color=(1, 0.6, 0.2))
    return extents

def differenceGraph(items, difference):
    size = items[0] + items[1]
    extents = [0, size, 0, size, 0, 0]
    m.surf(n.zeros((101, 101)), extent=extents, opacity=0.1)
    extents[4], extents[5] = n.min(difference), n.max(difference)
    m.surf(difference, extent=extents)
    return extents

def specificGraph(x, y, items, difference, specific, specificCondition):
    size = items[0] + items[1]
    X, Y = (n.full(101, round(specificCondition, 2)), y)
    extents = [X[0] * size, X[0] * size, 0, size, n.min(difference), n.max(difference)]
    if specific == 1:
        (X, Y) = (Y, X)
        extents[0:4] = (0, size, Y[0] * size, Y[0] * size)
    Z = n.mgrid[0:size, 0:101][0]
    m.surf(X, Y, Z, extent=extents, opacity=0.7, color=(1, 1, 1))
    return differenceGraph(items, difference)

def showGraph(extents):
    axes = m.axes(extent=extents, ranges=[0, 100, 0, 100, extents[4], extents[5]], xlabel="First Item", ylabel="Second Item")
    m.outline(extent=extents)
    m.show()

items = [0, 0]
while True:
    calculation = int(input("Choose Option:\n1. Compare value of reparing against selling\n2. Compare the value added by repairing\n3. Compare for a specific item\n"))
    items[0] = int(input("Enter the base value of the first item: "))
    items[1] = int(input("Enter the base value of the second item: "))
    skill = int(input("Enter your repair skill: "))
    x, y, added, repaired, difference, highVal = initialise(items)
    generate(items, added, repaired, difference, highVal)
    if calculation == 1: extents = compareGraph(items, added, repaired)
    elif calculation == 2: extents = differenceGraph(items, difference)
    elif calculation == 3:
        specific = int(input("Enter item with specific value (1/2): ")) - 1
        specificCondition = (int(input("Enter the current value of this item: ")) / items[specific]) ** (2/3)
        extents = specificGraph(x, y, items, difference, specific, specificCondition)
    showGraph(extents)

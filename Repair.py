from mayavi import mlab as m
import numpy as n

'''
Shapes three surfaces to
indicate the following:
1. The sell value of the
two items separately
2. The sell value of the
item resultant from repairing
the two items together
3. The difference between
the above values
'''
def generateSurfaces(itemValues):
    xAxis = n.linspace(0, 1, 101)
    yAxis = n.linspace(0, 1, 101)

    #Each surface is a 2D array of points at different altitudes
    addedSurface = n.zeros((101, 101))
    repairedSurface = n.zeros((101, 101))
    differenceSurface = n.zeros((101, 101))

    #Loop through each coordinate to set its altitude
    for x in range(101):
        for y in range(101):
            addedSurface[x][y] = xAxis[x] ** 1.5 * itemValues[0] + yAxis[y] ** 1.5 * itemValues[1]

            high, low = (xAxis[x], yAxis[y]) if xAxis[x] > yAxis[y] else (yAxis[y], xAxis[x])
            repairedSurface[x][y] = (n.min([(0.05 + (0.15 * (skill / 100))
            + high + (low * 0.05)), 1]) ** 1.5) * n.max([itemValues[0], itemValues[1]])
            
            differenceSurface[x][y] = repairedSurface[x][y] - addedSurface[x][y]
            
    return addedSurface, repairedSurface, differenceSurface

'''
Plots two surfaces
on the same axes
for comparison
'''
def compareGraph(itemValues, addedSurface, repairedSurface):
    #Size value is used to scale the shape such that the axes are of equal length
    size = itemValues[0] + itemValues[1]

    #Surface scaling
    extents = [0, size, 0, size, repairedSurface[0][0], repairedSurface[100][100]]

    m.surf(repairedSurface, extent=extents, color=(0.2, 0.4, 1))

    extents[4], extents[5] = 0, size
    m.surf(addedSurface, extent=extents, color=(1, 0.6, 0.2))

    return extents

'''
Plots a surface to
represent the difference
in value between repairing
items and selling them
directly. Also plots a
flat surface at value = 0
to indicate where profit
becomes loss
'''
def differenceGraph(itemValues, differenceSurface):
    #Size value is used to scale the shape such that the axes are of equal length
    size = itemValues[0] + itemValues[1]

    #Surface scaling
    extents = [0, size, 0, size, 0, 0]

    m.surf([[0,0],[0,0]], extent=extents, opacity=0.1)

    extents[4], extents[5] = n.min(differenceSurface), n.max(differenceSurface)
    m.surf(differenceSurface, extent=extents)

    return extents

'''
Plots a surface to
represent the difference
in value between repairing
items and selling them
directly. Also plots a
flat surface at value = 0
to indicate where profit
becomes loss, and a flat
surface at the condition
specified by the user
'''
def specificGraph(itemValues, differenceSurface, specific, specificCondition):
    #Size value is used to scale the shape such that the axes are of equal length
    size = itemValues[0] + itemValues[1]

    #Scales the flat surface to be parallel with the x / y axis depending on which item is specified
    if specific == 0:
        extents = [specificCondition * size, specificCondition * size, 0, size, n.min(differenceSurface), n.max(differenceSurface)]
        m.surf([[0, 0], [1, 1]], extent=extents, opacity=0.7, color=(1, 1, 1))
    else:
        extents = [0, size, specificCondition * size, specificCondition * size, n.min(differenceSurface), n.max(differenceSurface)]
        m.surf([[0, 1], [0, 1]], extent=extents, opacity=0.7, color=(1, 1, 1))

    return differenceGraph(itemValues, differenceSurface)

'''
Creates and
displays the graph
'''
def showGraph(extents, xLabel: str, yLabel: str):
    axes = m.axes(extent=extents, ranges=[0, 100, 0, 100, extents[4], extents[5]], xlabel=xLabel, ylabel=yLabel, zlabel="Cap Value")
    axes.label_text_property.font_size = 11
    m.outline(extent=extents)
    m.show()

'''
Requests user input repeatedly
until a number is entered
'''
def getNumber(message: str, low: int = None, high: int = None):
    while True:
        inp = input(message)
        if inp.isnumeric():
            if low is not None and int(inp) < low:
                print("Value is too low")
                continue
            if high is not None and int(inp) > high:
                print("Value is too high")
                continue
            return int(inp)
        else: print("Please enter a number")

while True:
    itemValues = [0, 0]
    itemNames = ["", ""]

    calculation = getNumber("Choose Option:\n1. Compare value of reparing against selling\n2. View the value added / lost by repairing\n3. View the value added / lost by repairing a specific item\n", 1, 3)
    itemNames[0] = input("Enter the name of the first item: ")
    itemValues[0] = getNumber("Enter the cap value of the first item in perfect condition: ", 0)
    itemNames[1] = input("Enter the name of the second item: ")
    itemValues[1] = getNumber("Enter the cap value of the second item in perfect condition: ", 0)
    skill = getNumber("Enter your repair skill: ", 0, 100)

    addedSurface, repairedSurface, differenceSurface = generateSurfaces(itemValues)

    if calculation == 1: extents = compareGraph(itemValues, addedSurface, repairedSurface)
    elif calculation == 2: extents = differenceGraph(itemValues, differenceSurface)
    elif calculation == 3:
        specific = getNumber("Which item's value would you like to specify? (1 or 2): ", 1, 2) - 1
        specificCondition = (getNumber("Enter the current value of this item: ", 0, itemValues[specific]) / itemValues[specific]) ** (2/3)
        extents = specificGraph(itemValues, differenceSurface, specific, specificCondition)

    showGraph(extents, itemNames[0], itemNames[1])

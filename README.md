# New-Vegas-Repair-Calculator

## Fallout: New Vegas Repair System
In the game Fallout: New Vegas, weapons and armour used by the player degrade over time. This affects practical stats such as damage and defence, but also the monetary value of the items in question. One way to make money in the game is to buy degraded items from vendors (or harvest them from enemies), repair them using another copy of the same item, and sell the result for a profit. For example, repairing two 10mm Pistols in low condition will result in a single 10mm Pistol in higher condition and potentially at a higher total value.

The relationship between condition and value is non-linear and is affected by the player's repair skill; it may not be obvious, therefore, whether repairing two items and selling the result will actually generate more revenue over simply selling the two items separately. The issue is complicated further by the 'Jury Rigging' perk, which allows the player to combine items that are merely similar rather than identical. The highly-valued 12.7mm Pistol, for example, can be repaired with the much cheaper 9mm Pistol for significant profit.

## Calulator
This calculator takes the player's repair skill, along with the base values of two items from the game, and produces graphs to indicate when it is profitable to repair them. For each graph, the X and Y axes each account for the condition of one of the items. The following three graphs are available:
### Compare value of reparing against selling
This function produces a 3D graph containing two 2D surfaces: the Z-value of the blue surface indicates the monetary value of the item resultant from repair, and the Z-value of the orange indicates the total monetary value of the two items separately. The highest of the two surfaces, therefore, indicates which is more profitable.
### View the value added / lost by repairing
This function produces a 3D graph containing a heatmapped 2D surface. The Z-value of this surface indicates the profit (or loss) of repairing the given items. A flat, transparent surface is generated at value = 0 to show the point at which profit becomes loss.
### View the value added / lost by repairing a specific item
The function takes an additional parameter: rather than just taking the base values of both items and showing a graph with all possible combinations, this function takes the current value of one of the items as well. It then produces the same graph as the above function, however it adds a second flat plane to show the current value of the item. The line along which this intersects with the heatmapped surface indicates the profit (or loss) of repairing one item with another at a specific value.

### Requirements
Python 3.13.1
Numpy 2.2.4
Mayavi 4.8.4

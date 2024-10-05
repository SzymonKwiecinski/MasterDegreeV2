import pulp
import math
import json

# Load data
data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)  # Number of depots
J = len(numport)   # Number of ports

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum([pulp.lpSum([x[i, j] for j in range(J)]) / 2 * price * distance[i][j] for i in range(I) for j in range(J)])

# Supply constraints
for i in range(I):
    problem += pulp.lpSum([x[i, j] for j in range(J)]) <= numdepot[i]

# Demand constraints
for j in range(J):
    problem += pulp.lpSum([x[i, j] for i in range(I)]) >= numport[j]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
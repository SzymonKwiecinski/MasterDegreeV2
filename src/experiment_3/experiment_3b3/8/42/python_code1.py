import pulp
import math
import json

# Load the data
data = json.loads('{"numdepot": [3, 3, 4], "numport": [1, 6, 3], "price": 3.0, "distance": [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}')

numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)
J = len(numport)

# Create the problem
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Decision variables
number = pulp.LpVariable.dicts("number", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(price * distance[i][j] * (number[i, j] / 2) for i in range(I) for j in range(J))

# Constraints
# Supply constraints at each depot
for i in range(I):
    problem += pulp.lpSum(number[i, j] for j in range(J)) <= numdepot[i]

# Demand constraints at each port
for j in range(J):
    problem += pulp.lpSum(number[i, j] for i in range(I)) >= numport[j]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp
import json

# Data in JSON format
data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

# Parameters
numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)  # number of depots
J = len(numport)   # number of ports

# Create the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(I) for j in range(J)), lowBound=0)

# Objective function
problem += pulp.lpSum((x[i, j] / 2) * price * distance[i][j] for i in range(I) for j in range(J))

# Constraints
for i in range(I):
    problem += pulp.lpSum(x[i, j] for j in range(J)) <= numdepot[i], f"DepotLimit_{i}"

for j in range(J):
    problem += pulp.lpSum(x[i, j] for i in range(I)) >= numport[j], f"PortDemand_{j}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
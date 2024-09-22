import pulp
import json

data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

# Extracting data from JSON
numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)  # Number of depots
J = len(numport)   # Number of ports

# Create the model
problem = pulp.LpProblem("Minimize_Transportation_Cost", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(I), range(J)), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum([x[i][j] * distance[i][j] * price / 2 for i in range(I) for j in range(J)]), "Total_Cost"

# Supply constraints (depots)
for i in range(I):
    problem += pulp.lpSum([x[i][j] for j in range(J)]) <= numdepot[i], f"Supply_Constraint_{i}"

# Demand constraints (ports)
for j in range(J):
    problem += pulp.lpSum([x[i][j] for i in range(I)]) >= numport[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Prepare output in the specified format
output = {
    "number": [[int(x[i][j].value()) for j in range(J)] for i in range(I)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
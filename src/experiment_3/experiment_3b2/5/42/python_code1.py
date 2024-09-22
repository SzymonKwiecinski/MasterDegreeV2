import pulp
import json

# Data provided in JSON format
data = {
    'numdepot': [3, 3, 4],
    'numport': [1, 6, 3],
    'price': 3.0,
    'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]
}

# Extracting data
numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

I = len(numdepot)  # Number of depots
J = len(numport)   # Number of ports

# Create the linear programming problem
problem = pulp.LpProblem("ContainerTransport", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(I), range(J)), lowBound=0)

# Objective Function
problem += pulp.lpSum((x[i][j] * price * distance[i][j]) / 2 for i in range(I) for j in range(J)), "TotalTransportationCost"

# Supply Constraints
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) <= numdepot[i], f"SupplyConstraint_{i}"

# Demand Constraints
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) == numport[j], f"DemandConstraint_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
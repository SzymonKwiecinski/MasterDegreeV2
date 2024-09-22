import pulp
import json

# Data in JSON format
data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

# Extract data from JSON
numdepot = data['numdepot']
numport = data['numport']
price = data['price']
distance = data['distance']

# Sets
I = len(numdepot)
J = len(numport)

# Create the linear programming problem
problem = pulp.LpProblem("ContainerTransportation", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(I), range(J)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum((x[i][j] / 2) * distance[i][j] * price for i in range(I) for j in range(J)), "TotalTransportationCost"

# Supply Constraints
for i in range(I):
    problem += pulp.lpSum(x[i][j] for j in range(J)) <= numdepot[i], f"SupplyConstraintDepot_{i+1}"

# Demand Constraints
for j in range(J):
    problem += pulp.lpSum(x[i][j] for i in range(I)) >= numport[j], f"DemandConstraintPort_{j+1}"

# Solve the problem
problem.solve()

# Output the results
output = [[x[i][j].varValue for i in range(I)] for j in range(J)]
print("Number of containers sent from each depot to port:")
for j in range(J):
    print(f"Port {j+1}: ", output[j])

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
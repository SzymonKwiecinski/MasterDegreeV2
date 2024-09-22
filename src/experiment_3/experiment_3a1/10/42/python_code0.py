import pulp
import json

# Data input
data = json.loads("{'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}")

num_depots = len(data['numdepot'])
num_ports = len(data['numport'])
price = data['price']
distance = data['distance']
numdepot = data['numdepot']
numport = data['numport']

# Create the linear programming problem
problem = pulp.LpProblem("ContainerTransportOptimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(num_depots), range(num_ports)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum((x[i][j] / 2) * distance[i][j] * price for i in range(num_depots) for j in range(num_ports)), "TotalCost"

# Supply constraints
for i in range(num_depots):
    problem += pulp.lpSum(x[i][j] for j in range(num_ports)) <= numdepot[i], f"SupplyConstraintDepot{i}"

# Demand constraints
for j in range(num_ports):
    problem += pulp.lpSum(x[i][j] for i in range(num_depots)) >= numport[j], f"DemandConstraintPort{j}"

# Solve the problem
problem.solve()

# Output the results
result = [[x[i][j].varValue for j in range(num_ports)] for i in range(num_depots)]
print(f'number = {result}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
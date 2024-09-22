import pulp
import json

# Data input
data = {'numdepot': [3, 3, 4], 'numport': [1, 6, 3], 'price': 3.0, 'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]}

num_depots = len(data['numdepot'])
num_ports = len(data['numport'])
price_per_km = data['price']
distance = data['distance']

# Create a problem variable
problem = pulp.LpProblem("ContainerTransportation", pulp.LpMinimize)

# Decision variables: number of containers to send from depot i to port j
number = pulp.LpVariable.dicts("number", (range(num_depots), range(num_ports)), lowBound=0, cat='Continuous')

# Objective function: Minimize total transportation cost
problem += pulp.lpSum(price_per_km * distance[i][j] * (number[i][j] / 2) for i in range(num_depots) for j in range(num_ports))

# Constraints
# Supply constraints (depot capacity)
for i in range(num_depots):
    problem += pulp.lpSum(number[i][j] for j in range(num_ports)) <= data['numdepot'][i]

# Demand constraints (port requirements)
for j in range(num_ports):
    problem += pulp.lpSum(number[i][j] for i in range(num_depots)) >= data['numport'][j]

# Solve the problem
problem.solve()

# Prepare output
output = {
    "number": [[int(number[i][j].varValue) for j in range(num_ports)] for i in range(num_depots)]
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print output
print(json.dumps(output))
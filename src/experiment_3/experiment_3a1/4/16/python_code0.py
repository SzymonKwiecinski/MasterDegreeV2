import pulp
import json

# Data provided in JSON format
data = json.loads("{'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}")

# Extracting parameters from the data
O = data['O']  # Number of crude oil types
P = data['P']  # Number of products
L = data['L']  # Number of processes
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output_data = data['Output']
cost = data['Cost']

# Define the problem
problem = pulp.LpProblem("OilRefineryProduction", pulp.LpMaximize)

# Define decision variables
x = pulp.LpVariable.dicts("x", range(1, L + 1), lowBound=0, cat='Continuous')

# Objective function
revenue = pulp.lpSum([price[p-1] * output_data[l-1][p-1] * x[l] for l in range(1, L + 1) for p in range(1, P + 1)]) 
cost_total = pulp.lpSum([cost[l-1] * pulp.lpSum([output_data[l-1][p-1] * x[l] for p in range(1, P + 1)]) for l in range(1, L + 1)])
problem += revenue - cost_total

# Constraints
for i in range(1, O + 1):
    problem += pulp.lpSum([input_data[l-1][i-1] * x[l] for l in range(1, L + 1)]) <= allocated[i - 1], f"SupplyConstraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp
import json

# Data input
data = json.loads("{'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}")

# Extracting data
O = data['O']  # Number of crude oil types
P = data['P']  # Number of products
L = data['L']  # Number of processes
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output_data = data['Output']

# Create the problem
problem = pulp.LpProblem("OilRefineryOptimization", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("ProcessExecution", range(1, L + 1), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(price[p] * pulp.lpSum(output_data[l-1][p] * x[l] for l in range(1, L + 1)) for p in range(P)), "TotalRevenue"

# Resource constraints
for i in range(O):
    problem += pulp.lpSum(input_data[l-1][i] * x[l] for l in range(1, L + 1)) <= allocated[i], f"ResourceConstraint_{i + 1}"

# Solve the problem
problem.solve()

# Output the results
revenue = pulp.value(problem.objective)
execution_plan = [x[l].varValue for l in range(1, L + 1)]

# Print objective value and execution plan
print(f' (Objective Value): <OBJ>{revenue}</OBJ>')
print(f'Execution plan: {execution_plan}')
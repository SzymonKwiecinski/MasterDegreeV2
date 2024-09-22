import pulp
import json

# Data provided in JSON format
data = json.loads('{"O": 2, "P": 2, "L": 3, "Allocated": [8000, 5000], "Price": [38, 33], "Input": [[3, 5], [1, 1], [5, 3]], "Output": [[4, 3], [1, 1], [3, 4]], "Cost": [51, 11, 40]}')

# Extract specific data
O = data['O']  # Number of crude oil types
P = data['P']  # Number of products
L = data['L']  # Number of processes
allocated = data['Allocated']  # Allocated crude oil
price = data['Price']  # Prices of products
input_data = data['Input']  # Input data
output_data = data['Output']  # Output data
cost = data['Cost']  # Costs of processes

# Problem definition
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(1, L + 1), lowBound=0)

# Objective function
revenue = pulp.lpSum((pulp.lpSum(output_data[l-1][p-1] * x[l] for l in range(1, L + 1)) * price[p-1] for p in range(1, P + 1))) 
costs = pulp.lpSum(cost[l-1] * (pulp.lpSum(output_data[l-1][p-1] * x[l] for p in range(1, P + 1))) for l in range(1, L + 1))
problem += revenue - costs, "Total_Revenue"

# Constraints
for i in range(1, O + 1):
    problem += pulp.lpSum(input_data[l-1][i-1] * x[l] for l in range(1, L + 1)) <= allocated[i-1], f"Crude_Oil_Constraint_{i}"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
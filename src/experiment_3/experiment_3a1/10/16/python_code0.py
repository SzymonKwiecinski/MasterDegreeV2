import pulp
import json

# Data input
data = json.loads('{"O": 2, "P": 2, "L": 3, "Allocated": [8000, 5000], "Price": [38, 33], "Input": [[3, 5], [1, 1], [5, 3]], "Output": [[4, 3], [1, 1], [3, 4]], "Cost": [51, 11, 40]}')

O = data['O']  # Total number of crude oil types
P = data['P']  # Total number of products
L = data['L']  # Total number of production processes
allocated = data['Allocated']
price = data['Price']
input_matrix = data['Input']
output_matrix = data['Output']
cost = data['Cost']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("Process", range(1, L + 1), lowBound=0, cat='Continuous')

# Objective function
revenue = pulp.lpSum(price[p] * pulp.lpSum(output_matrix[l-1][p] * x[l] for l in range(1, L + 1)) for p in range(P))
problem += revenue

# Constraints for crude oil usage
for i in range(O):
    problem += pulp.lpSum(input_matrix[l-1][i] * x[l] for l in range(1, L + 1)) <= allocated[i]

# Solve the problem
problem.solve()

# Output results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
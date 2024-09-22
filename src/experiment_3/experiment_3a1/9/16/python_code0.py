import pulp
import json

# Data input as JSON
data = json.loads('{"O": 2, "P": 2, "L": 3, "Allocated": [8000, 5000], "Price": [38, 33], "Input": [[3, 5], [1, 1], [5, 3]], "Output": [[4, 3], [1, 1], [3, 4]], "Cost": [51, 11, 40]}')

# Parameters
O = data['O']  # Number of crude oil types
P = data['P']  # Number of products
L = data['L']  # Number of production processes
allocated = data['Allocated']  # Allocated crude oil
price = data['Price']  # Selling price per product
input_matrix = data['Input']  # Input matrix for crude oil
output_matrix = data['Output']  # Output matrix for products
cost = data['Cost']  # Cost per process

# Create the LP problem
problem = pulp.LpProblem("Oil_Refinery_Optimization", pulp.LpMaximize)

# Decision Variables
execute = pulp.LpVariable.dicts("Execute", range(L), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(price[p] * pulp.lpSum(output_matrix[l][p] * execute[l] for l in range(L)) for p in range(P)), "Total_Revenue"

# Constraints for crude oil allocations
for i in range(O):
    problem += pulp.lpSum(input_matrix[l][i] * execute[l] for l in range(L)) <= allocated[i], f"Crude_Oil_Constraint_{i}"

# Solve the problem
problem.solve()

# Output the results
revenue = pulp.value(problem.objective)
execution_plan = [execute[l].varValue for l in range(L)]
print(f' (Objective Value): <OBJ>{revenue}</OBJ>')
print(f'Execution Plan: {execution_plan}')
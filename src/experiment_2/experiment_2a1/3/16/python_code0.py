import pulp
import json

data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}

# Extracting data from the input
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output_data = data['Output']
cost = data['Cost']
L = data['L']
O = data['O']
P = data['P']

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
execute = [pulp.LpVariable(f'execute_{l}', lowBound=0) for l in range(L)]

# Objective function
revenue = pulp.lpSum((pulp.lpSum(output_data[l][p] * execute[l] for l in range(L)) * price[p] for p in range(P)))
total_cost = pulp.lpSum((cost[l] * pulp.lpSum(execute[l]) for l in range(L)))
problem += revenue - total_cost, "Total_Profit"

# Constraints
for i in range(O):
    problem += pulp.lpSum(input_data[l][i] * execute[l] for l in range(L)) <= allocated[i], f"Crude_Oil_Constraint_{i}"

# Solve the problem
problem.solve()

# Collect results
revenue_value = pulp.value(problem.objective)
execute_values = [pulp.value(execute[l]) for l in range(L)]

# Output
output = {
    "revenue": revenue_value,
    "execute": execute_values
}

print(f' (Objective Value): <OBJ>{revenue_value}</OBJ>')
print(output)
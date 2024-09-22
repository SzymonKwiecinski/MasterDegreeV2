import pulp
import json

# Given data in JSON format
data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}

# Extracting relevant data
O = data['O']  # Number of crude types
P = data['P']  # Number of products
L = data['L']  # Number of processes
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output_data = data['Output']
cost = data['Cost']

# Create the LINear Programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: how many times to execute each process
execute = [pulp.LpVariable(f'execute_{l}', lowBound=0) for l in range(L)]

# Objective function: maximize revenue - cost
revenue = pulp.lpSum([output_data[l][p] * price[p] * execute[l] for l in range(L) for p in range(P)])
total_cost = pulp.lpSum([cost[l] * execute[l] for l in range(L)])
problem += revenue - total_cost, "Total_Profit"

# Constraints for resources
for i in range(O):
    problem += pulp.lpSum([input_data[l][i] * execute[l] for l in range(L)]) <= allocated[i], f"Resource_Constraint_{i}"

# Solve the problem
problem.solve()

# Collecting the results
revenue_value = pulp.value(problem.objective)
executions = [pulp.value(execute[l]) for l in range(L)]

# Output results
result = {
    "revenue": revenue_value,
    "execute": executions
}

# Printing the objective value
print(f' (Objective Value): <OBJ>{revenue_value}</OBJ>')
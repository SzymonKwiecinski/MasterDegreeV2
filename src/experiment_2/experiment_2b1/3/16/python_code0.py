import pulp
import json

# Input data in JSON format
data = {
    'O': 2,
    'P': 2,
    'L': 3,
    'Allocated': [8000, 5000],
    'Price': [38, 33],
    'Input': [[3, 5], [1, 1], [5, 3]],
    'Output': [[4, 3], [1, 1], [3, 4]],
    'Cost': [51, 11, 40]
}

# Problem parameters
O = data['O']  # Number of crude oil types
P = data['P']  # Number of products
L = data['L']  # Number of processes

allocated = data['Allocated']
price = data['Price']
input_l = data['Input']
output_l = data['Output']
cost_l = data['Cost']

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables for number of times to execute each process
execute_l = [pulp.LpVariable(f'execute_{l}', lowBound=0) for l in range(L)]

# Objective function: Maximize revenue - cost
revenue = pulp.lpSum([output_l[l][p] * execute_l[l] * price[p] for l in range(L) for p in range(P)])
cost = pulp.lpSum([cost_l[l] * execute_l[l] for l in range(L)])
problem += revenue - cost, "Total_Profit"

# Constraints for each crude oil type
for i in range(O):
    problem += pulp.lpSum([input_l[l][i] * execute_l[l] for l in range(L)]) <= allocated[i], f"Oil_Constraint_{i}"

# Solve the problem
problem.solve()

# Retrieve results
revenue_value = pulp.value(problem.objective)
execute_values = [pulp.value(execute_l[l]) for l in range(L)]

# Output result
result = {
    "revenue": revenue_value,
    "execute": execute_values
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
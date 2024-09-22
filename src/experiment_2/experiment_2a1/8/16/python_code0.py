import pulp
import json

data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}

# Extract data from the input
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output_data = data['Output']
cost = data['Cost']

# Initialize the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Define decision variables for how many times each process is executed
execute = [pulp.LpVariable(f'execute_{l}', lowBound=0) for l in range(L)]

# Objective function: Maximize total revenue minus total cost
revenue_expression = pulp.lpSum((output_data[l][p] * price[p] for l in range(L) for p in range(P)) * execute[l])
cost_expression = pulp.lpSum((output_data[l][p] * cost[l] for l in range(L)) * execute[l])
problem += revenue_expression - cost_expression, "Total_Profit"

# Constraints
for i in range(O):
    problem += pulp.lpSum((input_data[l][i] * execute[l] for l in range(L))) <= allocated[i], f"Input_limit_crude_{i}"

# Solve the problem
problem.solve()

# Prepare Output
revenue = pulp.value(problem.objective)
execute_values = [execute[l].varValue for l in range(L)]

# Print the results
print(f' (Objective Value): <OBJ>{revenue}</OBJ>')
output = {
    "revenue": revenue,
    "execute": execute_values
}
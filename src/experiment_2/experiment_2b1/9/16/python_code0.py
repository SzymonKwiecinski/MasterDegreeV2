import pulp
import json

data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}

# Extracting input data from the JSON
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output_data = data['Output']
cost = data['Cost']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Variables for the number of times each process is executed
execute = [pulp.LpVariable(f'execute_{l}', lowBound=0) for l in range(L)]

# Objective function: maximize total revenue
revenue = pulp.lpSum((output_data[l][p] * price[p] - cost[l]) * execute[l] for l in range(L) for p in range(P))
problem += revenue, "Total_Revenue"

# Constraints for the allocated crude oil
for i in range(O):
    problem += pulp.lpSum(input_data[l][i] * execute[l] for l in range(L)) <= allocated[i], f"Crude_Oil_Constraint_{i}"

# Solve the problem
problem.solve()

# Prepare the output
revenue_value = pulp.value(problem.objective)
execute_values = [execute[l].varValue for l in range(L)]

output_result = {
    "revenue": revenue_value,
    "execute": execute_values
}

print(json.dumps(output_result))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
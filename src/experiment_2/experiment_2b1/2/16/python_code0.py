import pulp
import json

data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}

# Extracting data
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_matrix = data['Input']
output_matrix = data['Output']
cost = data['Cost']

# Create the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
execute = [pulp.LpVariable(f'execute_{l}', lowBound=0) for l in range(L)]

# Objective function: Maximize revenue
revenue = pulp.lpSum((pulp.lpSum(output_matrix[l][p] * price[p] for p in range(P)) - pulp.lpSum(cost[l] * output_matrix[l][p] for p in range(P))) * execute[l] for l in range(L))
problem += revenue

# Constraints: Input constraints for each crude oil type
for i in range(O):
    problem += (pulp.lpSum(input_matrix[l][i] * execute[l] for l in range(L)) <= allocated[i]), f"Input_Constraint_{i}"

# Solve the problem
problem.solve()

# Prepare output
revenue_value = pulp.value(problem.objective)
execute_values = [pulp.value(execute[l]) for l in range(L)]

output = {
    "revenue": revenue_value,
    "execute": execute_values
}

print(json.dumps(output)) # Output in the specified format
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
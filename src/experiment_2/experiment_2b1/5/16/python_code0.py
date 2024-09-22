import pulp
import json

# Input data
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

# Prepare data
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output_data = data['Output']
cost = data['Cost']

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
execute = pulp.LpVariable.dicts("execute", range(L), lowBound=0)

# Objective function
revenue = pulp.lpSum([(pulp.lpSum([(output_data[l][p] * execute[l]) for l in range(L)])) * price[p] for p in range(P)])
problem += revenue - pulp.lpSum([cost[l] * execute[l] for l in range(L)])

# Constraints
for i in range(O):
    problem += pulp.lpSum([input_data[l][i] * execute[l] for l in range(L)]) <= allocated[i], f"Resource_Constraint_{i}"

# Solve the problem
problem.solve()

# Prepare the output
revenue_value = pulp.value(problem.objective)
execute_values = [execute[l].varValue for l in range(L)]

# Output the results
output = {
    "revenue": revenue_value,
    "execute": execute_values
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(json.dumps(output))
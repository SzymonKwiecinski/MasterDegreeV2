import pulp
import json

data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}

# Extract data
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

# Decision variables: how many times each process is executed
execute = pulp.LpVariable.dicts("Execute", range(L), lowBound=0, cat='Continuous')

# Objective function
revenue = pulp.lpSum([execute[l] * (pulp.lpSum([output_data[l][p] * price[p] for p in range(P)]) - pulp.lpSum([cost[l] * output_data[l][p] for p in range(P)])) for l in range(L)])

problem += revenue

# Constraints for crude oil allocation
for i in range(O):
    problem += pulp.lpSum([input_data[l][i] * execute[l] for l in range(L)]) <= allocated[i]

# Solve the problem
problem.solve()

# Output results
revenue_value = pulp.value(problem.objective)
execute_values = [pulp.value(execute[l]) for l in range(L)]

result = {
    "revenue": revenue_value,
    "execute": execute_values
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
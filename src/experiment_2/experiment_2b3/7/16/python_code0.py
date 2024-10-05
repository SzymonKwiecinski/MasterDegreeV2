import pulp

# Extracting data from the JSON
data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output = data['Output']
cost = data['Cost']

# Create the problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Create the variables for the number of times each process is executed
execute = [pulp.LpVariable(f'execute_{l}', lowBound=0, cat='Continuous') for l in range(L)]

# Objective function: Maximize revenue
# Revenue for each process l is: Sum(p)(output_l_p * price_p) - execute_l * cost_l
revenue = [pulp.lpSum(output[l][p] * price[p] for p in range(P)) * execute[l] - execute[l] * cost[l] for l in range(L)]
problem += pulp.lpSum(revenue)

# Constraints: Total input of crude oil i from all processes should not exceed allocated_i
for i in range(O):
    problem += pulp.lpSum(input_data[l][i] * execute[l] for l in range(L)) <= allocated[i]

# Solve the problem
problem.solve()

# Extracting the results
execute_values = [pulp.value(execute[l]) for l in range(L)]
revenue_value = pulp.value(problem.objective)

output_result = {
    "revenue": revenue_value,
    "execute": execute_values
}

print(output_result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
from pulp import LpProblem, LpMaximize, LpVariable, lpSum, value

# Problem data
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

# Unpacking the data
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
inputs = data['Input']
outputs = data['Output']
cost = data['Cost']

# Define the LP problem
problem = LpProblem("Maximize_Revenue", LpMaximize)

# Define decision variables
execute = [LpVariable(f'execute_{l}', lowBound=0) for l in range(L)]

# Objective function: Maximize revenue
problem += lpSum(
    (lpSum(outputs[l][p] * price[p] for p in range(P)) - cost[l]) * execute[l] 
    for l in range(L)
)

# Constraints: Crude oil allocation
for i in range(O):
    problem += lpSum(inputs[l][i] * execute[l] for l in range(L)) <= allocated[i], f"Crude_Constraint_{i}"

# Solve the problem
problem.solve()

# Retrieve the results
revenue = value(problem.objective)
execute_values = [value(execute[l]) for l in range(L)]

# Output the results
output = {
    "revenue": revenue,
    "execute": execute_values
}

print(output)
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')
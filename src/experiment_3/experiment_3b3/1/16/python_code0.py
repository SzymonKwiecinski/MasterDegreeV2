import pulp

# Data
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

# Indices
O = data['O']
P = data['P']
L = data['L']

# Parameters
allocated = data['Allocated']
price = data['Price']
input_data = data['Input']
output = data['Output']
cost = data['Cost']

# Problem
problem = pulp.LpProblem('Oil_Refinery_Production', pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{l}', lowBound=0, cat='Continuous') for l in range(L)]

# Objective Function
objective = pulp.lpSum(price[p] * pulp.lpSum(output[l][p] * x[l] for l in range(L)) for p in range(P)) \
            - pulp.lpSum(cost[l] * pulp.lpSum(output[l][p] * x[l] for p in range(P)) for l in range(L))

problem += objective

# Constraints
for i in range(O):
    problem += (pulp.lpSum(input_data[l][i] * x[l] for l in range(L)) <= allocated[i])

# Solve
problem.solve()

# Results
revenue = pulp.value(problem.objective)
execute = [pulp.value(x[l]) for l in range(L)]

print(f'Revenue: {revenue}')
print(f'Execute: {execute}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
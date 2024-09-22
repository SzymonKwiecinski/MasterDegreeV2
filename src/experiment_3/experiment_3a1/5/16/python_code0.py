import pulp

# Data from JSON
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

# Parameters
O = data['O']
P = data['P']
L = data['L']
allocated = data['Allocated']
price = data['Price']
input_matrix = data['Input']
output_matrix = data['Output']
cost = data['Cost']

# Define the problem
problem = pulp.LpProblem("Oil_Refinery_Production", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("Process", range(L), lowBound=0)

# Objective Function
revenue = pulp.lpSum(price[p] * pulp.lpSum(output_matrix[l][p] * x[l] for l in range(L)) for p in range(P))
costs = pulp.lpSum(cost[l] * pulp.lpSum(output_matrix[l][p] * x[l] for p in range(P)) for l in range(L))
problem += revenue - costs

# Constraints
for i in range(O):
    problem += pulp.lpSum(input_matrix[l][i] * x[l] for l in range(L)) <= allocated[i]

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
for l in range(L):
    print(f'Process {l}: {x[l].varValue}')
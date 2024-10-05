import pulp

# Given data
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

# Define the problem
problem = pulp.LpProblem("Oil_Refinery_Optimization", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(data['L']), lowBound=0)

# Objective function
revenue = pulp.lpSum(data['Price'][p] * pulp.lpSum(data['Output'][l][p] * x[l] for l in range(data['L'])) for p in range(data['P']))
cost = pulp.lpSum(data['Cost'][l] * pulp.lpSum(data['Output'][l][p] * x[l] for p in range(data['P'])) for l in range(data['L']))
problem += revenue - cost

# Constraints
for i in range(data['O']):
    problem += pulp.lpSum(data['Input'][l][i] * x[l] for l in range(data['L'])) <= data['Allocated'][i]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
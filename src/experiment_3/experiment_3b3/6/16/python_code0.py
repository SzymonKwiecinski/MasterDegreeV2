import pulp

# Data from the JSON
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

# Initialize the problem
problem = pulp.LpProblem("Oil_Refinery_Production", pulp.LpMaximize)

# Decision variables
execute = [pulp.LpVariable(f'execute_{l}', lowBound=0, cat='Continuous') for l in range(data['L'])]

# Objective function: Maximize total revenue
revenue = pulp.lpSum(
    data['Price'][p] * pulp.lpSum(data['Output'][l][p] * execute[l] for l in range(data['L'])) for p in range(data['P'])
)
problem += revenue

# Constraints

# 1. Availability of crude oil
for i in range(data['O']):
    problem += pulp.lpSum(data['Input'][l][i] * execute[l] for l in range(data['L'])) <= data['Allocated'][i]

# Solve the problem
problem.solve()

# Output results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
for l, var in enumerate(execute):
    print(f'Execute process {l+1}: {pulp.value(var)}')
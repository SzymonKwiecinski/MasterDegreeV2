import pulp

# Data
data = {'O': 2, 'P': 2, 'L': 3, 'Allocated': [8000, 5000], 'Price': [38, 33], 'Input': [[3, 5], [1, 1], [5, 3]], 'Output': [[4, 3], [1, 1], [3, 4]], 'Cost': [51, 11, 40]}

# Problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision Variables
execute = [pulp.LpVariable(f'execute_{l}', lowBound=0, cat='Continuous') for l in range(data['L'])]

# Constraints
# Crude oil constraints
for i in range(data['O']):
    problem += (pulp.lpSum(data['Input'][l][i] * execute[l] for l in range(data['L'])) <= data['Allocated'][i])

# Objective function
profit = pulp.lpSum((pulp.lpSum(data['Price'][p] * data['Output'][l][p] for p in range(data['P'])) - data['Cost'][l]) * execute[l] for l in range(data['L']))
problem += profit

# Solve the problem
problem.solve()

# Results
revenue = pulp.value(problem.objective)
execute_values = [pulp.value(execute[l]) for l in range(data['L'])]

output = {
    "revenue": revenue,
    "execute": execute_values
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
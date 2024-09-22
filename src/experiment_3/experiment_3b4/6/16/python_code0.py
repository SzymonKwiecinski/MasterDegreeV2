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

# Problem
problem = pulp.LpProblem("Maximize_Total_Profit", pulp.LpMaximize)

# Variables
x = [pulp.LpVariable(f'x_{l+1}', lowBound=0) for l in range(data['L'])]

# Objective Function
revenue = sum(data['Price'][p] * sum(data['Output'][l][p] * x[l] for l in range(data['L'])) for p in range(data['P']))
costs = sum(data['Cost'][l] * sum(data['Output'][l][p] * x[l] for p in range(data['P'])) for l in range(data['L']))
problem += revenue - costs

# Constraints
for i in range(data['O']):
    problem += sum(data['Input'][l][i] * x[l] for l in range(data['L'])) <= data['Allocated'][i]

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
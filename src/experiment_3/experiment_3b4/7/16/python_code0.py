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

# Problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f"x_{l}", lowBound=0, cat='Continuous') for l in range(data['L'])]

# Objective Function
revenue = sum((sum(data['Output'][l][p] * data['Price'][p] for p in range(data['P'])) - data['Cost'][l]) * x[l] for l in range(data['L']))
problem += revenue

# Constraints
for i in range(data['O']):
    problem += sum(data['Input'][l][i] * x[l] for l in range(data['L'])) <= data['Allocated'][i]

# Solve
problem.solve()

# Objective Value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
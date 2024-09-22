import pulp

# Data
data = {
    'O': 2,
    'P': 2,
    'L': 3,
    'Allocated': [8000, 5000],
    'Price': [38, 33],
    'Input': [
        [3, 5],  # Inputs for L=1
        [1, 1],  # Inputs for L=2
        [5, 3]   # Inputs for L=3
    ],
    'Output': [
        [4, 3],  # Outputs for L=1
        [1, 1],  # Outputs for L=2
        [3, 4]   # Outputs for L=3
    ],
    'Cost': [51, 11, 40]
}

# Problem
problem = pulp.LpProblem("Oil_Refinery_Optimization", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{l}', lowBound=0) for l in range(data['L'])]

# Objective Function
objective = sum(
    (sum(data['Price'][p] * data['Output'][l][p] for p in range(data['P'])) - data['Cost'][l]) * x[l]
    for l in range(data['L'])
)
problem += objective

# Constraints
for i in range(data['O']):
    problem += sum(data['Input'][l][i] * x[l] for l in range(data['L'])) <= data['Allocated'][i]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
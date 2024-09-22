import pulp

# Data extracted from JSON format
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

# Initialize LP problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables: number of times process l is executed
x = [pulp.LpVariable(f'x_{l}', lowBound=0, cat='Continuous') for l in range(data['L'])]

# Objective function: Maximize revenue
revenue = pulp.lpSum(data['Price'][p] * pulp.lpSum(data['Output'][l][p] * x[l] for l in range(data['L'])) 
                     for p in range(data['P']))
problem += revenue

# Constraints: Resource constraints for each crude oil type
for i in range(data['O']):
    problem += pulp.lpSum(data['Input'][l][i] * x[l] for l in range(data['L'])) <= data['Allocated'][i]

# Solve the problem
problem.solve()

# Print the optimal objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp

# Data from the provided JSON
data = {
    'M': 4,
    'N': 5,
    'Available': [10, 20, 15, 35, 25],
    'Requirements': [
        [3, 2, 0, 0],
        [0, 5, 2, 1],
        [1, 0, 0, 5],
        [0, 3, 1, 1]
    ],
    'Prices': [7, 10, 5, 9]
}

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Revenue", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Continuous') for j in range(data['M'])]

# Objective function
problem += pulp.lpSum(data['Prices'][j] * x[j] for j in range(data['M']))

# Constraints
for i in range(data['N']):
    problem += pulp.lpSum(data['Requirements'][i][j] * x[j] for j in range(data['M'])) <= data['Available'][i]

# Solve the problem
problem.solve()

# Output the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp

# Data
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Number of products
M = len(data['prices'])

# Number of materials
N = len(data['available'])

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective function
profit = pulp.lpSum((data['prices'][j] - data['costs'][j]) * x[j] for j in range(M))
problem += profit

# Material availability constraints
for i in range(N):
    problem += pulp.lpSum(data['requirements'][i][j] * x[j] for j in range(M)) <= data['available'][i]

# Demand constraints
for j in range(M):
    problem += x[j] <= data['demands'][j]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
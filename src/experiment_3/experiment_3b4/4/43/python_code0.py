import pulp

# Data from JSON
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Number of products and raw materials
M = len(data['prices'])
N = len(data['available'])

# Define the Linear Programming problem
problem = pulp.LpProblem("Wild_Sports_Profit_Maximization", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective function: Maximize total profit
problem += pulp.lpSum((data['prices'][j] - data['costs'][j]) * x[j] for j in range(M))

# Constraints
# Raw material constraints
for i in range(N):
    problem += pulp.lpSum(data['requirements'][i][j] * x[j] for j in range(M)) <= data['available'][i]

# Demand constraints
for j in range(M):
    problem += x[j] <= data['demands'][j]

# Solve the problem
problem.solve()

# Print the Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
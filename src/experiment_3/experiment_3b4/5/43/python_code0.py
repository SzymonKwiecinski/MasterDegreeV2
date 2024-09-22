import pulp

# Data
data = {
    'available': [240000, 8000, 75000],
    'requirements': [
        [48, 1, 10], 
        [40, 1, 10], 
        [0, 1, 2]
    ],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Indices
M = len(data['prices'])  # Number of products
N = len(data['available'])  # Number of raw materials

# Initialize the problem
problem = pulp.LpProblem("Wild_Sports_Profit_Maximization", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective function
profit = pulp.lpSum((data['prices'][j] - data['costs'][j]) * x[j] for j in range(M))
problem += profit

# Material Constraints
for i in range(N):
    problem += pulp.lpSum(data['requirements'][i][j] * x[j] for j in range(M)) <= data['available'][i]

# Demand Constraints
for j in range(M):
    problem += x[j] <= data['demands'][j]

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
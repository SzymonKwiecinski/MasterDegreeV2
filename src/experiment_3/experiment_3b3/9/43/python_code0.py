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

# Problem
problem = pulp.LpProblem("WildSportsProfitMaximization", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective Function
profit = sum((data['prices'][j] - data['costs'][j]) * x[j] for j in range(M))
problem += profit

# Constraints
# Raw material constraints
for i in range(N):
    problem += sum(data['requirements'][i][j] * x[j] for j in range(M)) <= data['available'][i]

# Demand constraints
for j in range(M):
    problem += x[j] <= data['demands'][j]

# Solve Problem
problem.solve()

# Output Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
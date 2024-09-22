import pulp

# Given data
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Define the problem
problem = pulp.LpProblem("Wild_Sports_Profit_Maximization", pulp.LpMaximize)

# Variables
M = len(data['prices'])
amount = pulp.LpVariable.dicts("amount", range(M), lowBound=0)

# Objective function
profit = pulp.lpSum((data['prices'][j] - data['costs'][j]) * amount[j] for j in range(M))
problem += profit

# Material Constraints
N = len(data['available'])
for i in range(N):
    problem += pulp.lpSum(data['requirements'][i][j] * amount[j] for j in range(M)) <= data['available'][i]

# Demand Constraints
for j in range(M):
    problem += amount[j] <= data['demands'][j]

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
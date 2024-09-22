import pulp

# Data
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Parameters
M = len(data['prices'])
N = len(data['available'])

# Initialize the problem
problem = pulp.LpProblem("Wild_Sports_Production", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x{j}', lowBound=0, cat='Continuous') for j in range(M)]

# Objective function
profit = [(data['prices'][j] - data['costs'][j]) for j in range(M)]
problem += pulp.lpSum(profit[j] * x[j] for j in range(M))

# Material constraints
for i in range(N):
    problem += pulp.lpSum(data['requirements'][i][j] * x[j] for j in range(M)) <= data['available'][i]

# Demand constraints
for j in range(M):
    problem += x[j] <= data['demands'][j]

# Solve the problem
problem.solve()

# Output the results
amount = [pulp.value(x[j]) for j in range(M)]
total_profit = pulp.value(problem.objective)

print(f'Amount: {amount}')
print(f'Total Profit (Objective Value): <OBJ>{total_profit}</OBJ>')
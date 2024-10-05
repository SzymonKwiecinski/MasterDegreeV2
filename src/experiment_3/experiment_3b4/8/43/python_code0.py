import pulp

# Data from the JSON
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Number of raw materials and products
N = len(data['available'])
M = len(data['prices'])

# LP Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
amount = {j: pulp.LpVariable(f'amount_{j}', lowBound=0, cat='Continuous') for j in range(M)}

# Objective function
profit = pulp.lpSum((data['prices'][j] - data['costs'][j]) * amount[j] for j in range(M))
problem += profit

# Constraints
# Raw material constraints
for i in range(N):
    problem += pulp.lpSum(data['requirements'][i][j] * amount[j] for j in range(M)) <= data['available'][i]

# Demand constraints
for j in range(M):
    problem += amount[j] <= data['demands'][j]

# Solve the problem
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
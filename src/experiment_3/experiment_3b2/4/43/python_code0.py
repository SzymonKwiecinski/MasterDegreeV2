import pulp

# Data
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Sets
M = range(len(data['prices']))  # Products
N = range(len(data['available']))  # Raw materials

# Create the problem
problem = pulp.LpProblem("Wild_Sports_Optimization", pulp.LpMaximize)

# Decision variables
amount = pulp.LpVariable.dicts("amount", M, lowBound=0)

# Objective function
profit = pulp.lpSum([(data['prices'][j] - data['costs'][j]) * amount[j] for j in M])
problem += profit

# Material constraints
for i in N:
    problem += pulp.lpSum([data['requirements'][i][j] * amount[j] for j in M]) <= data['available'][i]

# Demand constraints
for j in M:
    problem += amount[j] <= data['demands'][j]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp

# Data from JSON
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Define the problem
problem = pulp.LpProblem("Wild_Sports_Optimization", pulp.LpMaximize)

# Define decision variables
M = len(data['prices'])
x = pulp.LpVariable.dicts("Units_Produced", range(M), lowBound=0)

# Objective function
profit = [data['prices'][j] - data['costs'][j] for j in range(M)]
problem += pulp.lpSum(profit[j] * x[j] for j in range(M))

# Constraints
N = len(data['available'])
# Raw Material Availability Constraints
for i in range(N):
    problem += pulp.lpSum(data['requirements'][j][i] * x[j] for j in range(M)) <= data['available'][i]

# Demand Constraints
for j in range(M):
    problem += x[j] <= data['demands'][j]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
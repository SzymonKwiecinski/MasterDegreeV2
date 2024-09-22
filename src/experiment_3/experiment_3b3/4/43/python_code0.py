import pulp

# Data from the problem
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Number of products (M) and raw materials (N)
M = len(data['prices'])
N = len(data['available'])

# Create the problem variable
problem = pulp.LpProblem("Wild_Sports_Profit_Maximization", pulp.LpMaximize)

# Decision variables
amount = [pulp.LpVariable(f'amount_{j}', lowBound=0) for j in range(M)]

# Objective function
profit_contributions = [(data['prices'][j] - data['costs'][j]) * amount[j] for j in range(M)]
problem += pulp.lpSum(profit_contributions), "Total Profit"

# Constraints

# Raw material constraints
for i in range(N):
    problem += (
        pulp.lpSum(data['requirements'][i][j] * amount[j] for j in range(M)) <= data['available'][i],
        f"Raw_Material_Constraint_{i}"
    )

# Demand constraints
for j in range(M):
    problem += (amount[j] <= data['demands'][j], f"Demand_Constraint_{j}")

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
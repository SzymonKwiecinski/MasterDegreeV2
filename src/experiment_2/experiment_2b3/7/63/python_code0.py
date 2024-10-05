import pulp

# Data input
data = {'large_roll_width': 70, 'demands': [40, 65, 80, 75], 'roll_width_options': [17, 14, 11, 8.5], 'patterns': [[4, 0, 0, 0], [3, 1, 0, 0], [3, 0, 1, 0], [2, 2, 0, 0], [3, 0, 0, 2], [2, 1, 2, 0], [2, 1, 1, 1], [2, 1, 0, 2], [2, 0, 3, 0], [2, 0, 2, 1], [2, 0, 1, 2], [1, 3, 1, 0], [1, 3, 0, 1], [1, 2, 2, 0], [1, 2, 1, 1], [1, 2, 0, 2], [1, 1, 3, 0], [0, 5, 0, 0], [0, 4, 1, 0], [0, 4, 0, 1], [0, 3, 2, 0], [2, 0, 0, 4], [1, 1, 2, 2], [1, 1, 1, 3], [1, 1, 0, 4], [1, 0, 4, 1], [1, 0, 3, 2], [1, 0, 2, 3], [1, 0, 1, 4], [0, 3, 1, 2], [0, 3, 0, 3], [0, 2, 3, 1], [0, 2, 2, 2], [0, 2, 1, 3], [0, 2, 0, 4], [0, 1, 5, 0], [0, 1, 4, 1], [0, 1, 3, 2], [0, 0, 6, 0], [0, 0, 5, 1], [1, 0, 0, 6], [0, 1, 2, 4], [0, 1, 1, 5], [0, 1, 0, 6], [0, 0, 4, 3], [0, 0, 3, 4], [0, 0, 2, 5], [0, 0, 1, 6], [0, 0, 0, 8]]}

large_roll_width = data["large_roll_width"]
roll_width_options = data["roll_width_options"]
demands = data["demands"]
patterns = data["patterns"]

N = len(patterns)  # Number of patterns
M = len(roll_width_options)  # Number of roll widths

# Problem definition
problem = pulp.LpProblem("MinimizeLargeRolls", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', cat='Integer', lowBound=0) for i in range(N)]

# Objective function: minimize the number of large rolls used
problem += pulp.lpSum(x), "TotalLargeRolls"

# Constraints: satisfy the demand for each roll width
for j in range(M):
    problem += (pulp.lpSum(patterns[i][j] * x[i] for i in range(N)) >= demands[j], f"Demand_satisfaction_{j}")

# Solve the problem
problem.solve()

# Collect the results
patterns_used = [{"pattern": patterns[i], "amount": int(x[i].varValue)} for i in range(N) if x[i].varValue > 0]
total_large_rolls = sum(x[i].varValue for i in range(N))

result = {
    "patterns": patterns_used,
    "total_large_rolls_used": total_large_rolls
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp

# Data from the input
data = {
    "large_roll_width": 70,
    "demands": [40, 65, 80, 75],
    "roll_width_options": [17, 14, 11, 8.5],
    "patterns": [
        [4, 0, 0, 0], [3, 1, 0, 0], [3, 0, 1, 0], [2, 2, 0, 0], [3, 0, 0, 2], 
        [2, 1, 2, 0], [2, 1, 1, 1], [2, 1, 0, 2], [2, 0, 3, 0], [2, 0, 2, 1], 
        [2, 0, 1, 2], [1, 3, 1, 0], [1, 3, 0, 1], [1, 2, 2, 0], [1, 2, 1, 1], 
        [1, 2, 0, 2], [1, 1, 3, 0], [0, 5, 0, 0], [0, 4, 1, 0], [0, 4, 0, 1], 
        [0, 3, 2, 0], [2, 0, 0, 4], [1, 1, 2, 2], [1, 1, 1, 3], [1, 1, 0, 4], 
        [1, 0, 4, 1], [1, 0, 3, 2], [1, 0, 2, 3], [1, 0, 1, 4], [0, 3, 1, 2],
        [0, 3, 0, 3], [0, 2, 3, 1], [0, 2, 2, 2], [0, 2, 1, 3], [0, 2, 0, 4],
        [0, 1, 5, 0], [0, 1, 4, 1], [0, 1, 3, 2], [0, 0, 6, 0], [0, 0, 5, 1],
        [1, 0, 0, 6], [0, 1, 2, 4], [0, 1, 1, 5], [0, 1, 0, 6], [0, 0, 4, 3],
        [0, 0, 3, 4], [0, 0, 2, 5], [0, 0, 1, 6], [0, 0, 0, 8]
    ]
}

large_roll_width = data["large_roll_width"]
demands = data["demands"]
patterns = data["patterns"]

# Number of different widths and cutting patterns
M = len(demands)
N = len(patterns)

# Initialize the problem
problem = pulp.LpProblem("MinimizeLargeRolls", pulp.LpMinimize)

# Decision variables for the number of large rolls used for each pattern
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Integer') for i in range(N)]

# Objective function
problem += pulp.lpSum(x), "TotalLargeRollsUsed"

# Constraints to satisfy demand for each type of smaller rolls
for j in range(M):
    problem += pulp.lpSum(patterns[i][j] * x[i] for i in range(N)) >= demands[j], f"Demand_constraint_{j}"

# Solve the problem
problem.solve()

# Output the results
output_patterns = []
for i in range(N):
    if pulp.value(x[i]) > 0:
        output_patterns.append({"pattern": patterns[i], "amount": pulp.value(x[i])})

output = {
    "patterns": output_patterns,
    "total_large_rolls_used": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
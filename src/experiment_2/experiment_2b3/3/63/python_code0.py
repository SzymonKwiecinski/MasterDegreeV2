import pulp

# Problem data
data = {
    "large_roll_width": 70,
    "roll_width_options": [17, 14, 11, 8.5],
    "demands": [40, 65, 80, 75],
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
        [0, 0, 3, 4], [0, 0, 2, 5], [0, 0, 1, 6], [0, 0, 0, 8],
    ]
}

# Extracting data
large_roll_width = data["large_roll_width"]
roll_width_options = data["roll_width_options"]
demands = data["demands"]
patterns = data["patterns"]

# Indices
N = len(patterns)  # Number of patterns
M = len(roll_width_options)  # Number of different rolls

# Initialize the MILP problem
problem = pulp.LpProblem("Cutting_Stock_Problem", pulp.LpMinimize)

# Decision variables
pattern_vars = [pulp.LpVariable(f"Pattern_{i}", lowBound=0, cat='Integer') for i in range(N)]

# Objective: Minimize the number of large rolls used
problem += pulp.lpSum(pattern_vars)

# Constraints
for j in range(M):
    problem += pulp.lpSum(patterns[i][j] * pattern_vars[i] for i in range(N)) >= demands[j]

# Solve the problem
problem.solve()

# Output the result
patterns_used = [{"pattern": patterns[i], "amount": int(pulp.value(pattern_vars[i]))} for i in range(N) if pulp.value(pattern_vars[i]) > 0]

output = {
    "patterns": patterns_used,
    "total_large_rolls_used": int(pulp.value(problem.objective))
}

print("Output:", output)
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
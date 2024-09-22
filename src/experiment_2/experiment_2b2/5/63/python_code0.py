import pulp

# Data input
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
        [0, 0, 3, 4], [0, 0, 2, 5], [0, 0, 1, 6], [0, 0, 0, 8]
    ]
}

large_roll_width = data["large_roll_width"]
roll_width_options = data["roll_width_options"]
demands = data["demands"]
patterns = data["patterns"]
N = len(patterns)
M = len(roll_width_options)

# Initialize the problem
problem = pulp.LpProblem("Minimize_Large_Rolls_Used", pulp.LpMinimize)

# Decision variables
x_vars = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Integer') for i in range(N)]

# Objective: Minimize the number of large rolls used
problem += pulp.lpSum(x_vars)

# Constraints: Fulfill the demand for each type of roll
for j in range(M):
    problem += pulp.lpSum(patterns[i][j] * x_vars[i] for i in range(N)) >= demands[j]

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "patterns": [
        {"pattern": patterns[i], "amount": x_vars[i].varValue}
        for i in range(N) if x_vars[i].varValue > 0
    ],
    "total_large_rolls_used": pulp.value(problem.objective)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
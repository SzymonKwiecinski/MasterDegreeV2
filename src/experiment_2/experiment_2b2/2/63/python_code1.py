import pulp

# Data given in JSON format
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
M = len(data["demands"])  # Number of different roll widths
N = len(data["patterns"])  # Number of cutting patterns

# Problem
problem = pulp.LpProblem("Minimize_Large_Rolls", pulp.LpMinimize)

# Decision variables
use_pattern = [pulp.LpVariable(f"use_pattern_{i}", lowBound=0, cat='Continuous') for i in range(N)]

# Objective function
problem += pulp.lpSum(use_pattern), "Total_Large_Rolls_Used"

# Constraints
for j in range(M):
    problem += (pulp.lpSum(data["patterns"][i][j] * use_pattern[i] for i in range(N)) >= data["demands"][j]), f"Demand_for_roll_width_{data['roll_width_options'][j]}"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "patterns": [
        {
            "pattern": data["patterns"][i],
            "amount": pulp.value(use_pattern[i])
        }
        for i in range(N) if pulp.value(use_pattern[i]) > 0
    ],
    "total_large_rolls_used": pulp.value(problem.objective)
}

# Print the output
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
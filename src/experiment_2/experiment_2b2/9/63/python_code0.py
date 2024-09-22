import pulp

# Data from the JSON input
data = {
    'large_roll_width': 70,
    'demands': [40, 65, 80, 75],
    'roll_width_options': [17, 14, 11, 8.5],
    'patterns': [
        [4, 0, 0, 0], [3, 1, 0, 0], [3, 0, 1, 0], [2, 2, 0, 0],
        [3, 0, 0, 2], [2, 1, 2, 0], [2, 1, 1, 1], [2, 1, 0, 2],
        [2, 0, 3, 0], [2, 0, 2, 1], [2, 0, 1, 2], [1, 3, 1, 0],
        [1, 3, 0, 1], [1, 2, 2, 0], [1, 2, 1, 1], [1, 2, 0, 2],
        [1, 1, 3, 0], [0, 5, 0, 0], [0, 4, 1, 0], [0, 4, 0, 1],
        [0, 3, 2, 0], [2, 0, 0, 4], [1, 1, 2, 2], [1, 1, 1, 3],
        [1, 1, 0, 4], [1, 0, 4, 1], [1, 0, 3, 2], [1, 0, 2, 3],
        [1, 0, 1, 4], [0, 3, 1, 2], [0, 3, 0, 3], [0, 2, 3, 1],
        [0, 2, 2, 2], [0, 2, 1, 3], [0, 2, 0, 4], [0, 1, 5, 0],
        [0, 1, 4, 1], [0, 1, 3, 2], [0, 0, 6, 0], [0, 0, 5, 1],
        [1, 0, 0, 6], [0, 1, 2, 4], [0, 1, 1, 5], [0, 1, 0, 6],
        [0, 0, 4, 3], [0, 0, 3, 4], [0, 0, 2, 5], [0, 0, 1, 6],
        [0, 0, 0, 8]
    ]
}

large_roll_width = data['large_roll_width']
M = len(data['demands'])
N = len(data['patterns'])

# Create the problem
problem = pulp.LpProblem("Minimum_Large_Rolls", pulp.LpMinimize)

# Variables
patterns_use = [pulp.LpVariable(f'p_{i}', cat='Integer', lowBound=0) for i in range(N)]

# Objective
problem += pulp.lpSum(patterns_use)

# Constraints
for j in range(M):
    problem += pulp.lpSum(data['patterns'][i][j] * patterns_use[i] for i in range(N)) >= data['demands'][j]

# Solve the problem
problem.solve()

# Output formatting
result_patterns = []
for i in range(N):
    if patterns_use[i].varValue > 0:
        result_patterns.append({
            "pattern": data['patterns'][i],
            "amount": int(patterns_use[i].varValue)
        })

result = {
    "patterns": result_patterns,
    "total_large_rolls_used": int(pulp.value(problem.objective))
}

# Print the solution
print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
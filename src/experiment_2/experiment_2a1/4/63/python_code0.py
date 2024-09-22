import pulp
import json

# Input data
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

# Parameters
large_roll_width = data['large_roll_width']
demands = data['demands']
patterns = data['patterns']

# Number of demands and patterns
M = len(demands)
N = len(patterns)

# Create the optimization problem
problem = pulp.LpProblem("Minimize_Large_Rolls", pulp.LpMinimize)

# Decision variables: amount of each pattern to use
amounts = [pulp.LpVariable(f'amount_{i}', lowBound=0, cat='Integer') for i in range(N)]

# Objective function: minimize the total number of large rolls used
problem += pulp.lpSum(amounts)

# Constraints for each demand
for j in range(M):
    problem += pulp.lpSum(patterns[i][j] * amounts[i] for i in range(N)) >= demands[j]

# Solve the problem
problem.solve()

# Prepare output
output_patterns = [{'pattern': patterns[i], 'amount': int(amounts[i].varValue)} for i in range(N) if amounts[i].varValue > 0]
total_large_rolls_used = pulp.value(problem.objective)

# Output result
result = {
    "patterns": output_patterns,
    "total_large_rolls_used": int(total_large_rolls_used)
}

print(json.dumps(result, indent=2))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
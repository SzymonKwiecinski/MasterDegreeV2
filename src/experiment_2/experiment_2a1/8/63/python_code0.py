import pulp
import json

# Input Data
data = '{"large_roll_width": 70, "demands": [40, 65, 80, 75], "roll_width_options": [17, 14, 11, 8.5], "patterns": [[4, 0, 0, 0], [3, 1, 0, 0], [3, 0, 1, 0], [2, 2, 0, 0], [3, 0, 0, 2], [2, 1, 2, 0], [2, 1, 1, 1], [2, 1, 0, 2], [2, 0, 3, 0], [2, 0, 2, 1], [2, 0, 1, 2], [1, 3, 1, 0], [1, 3, 0, 1], [1, 2, 2, 0], [1, 2, 1, 1], [1, 2, 0, 2], [1, 1, 3, 0], [0, 5, 0, 0], [0, 4, 1, 0], [0, 4, 0, 1], [0, 3, 2, 0], [2, 0, 0, 4], [1, 1, 2, 2], [1, 1, 1, 3], [1, 1, 0, 4], [1, 0, 4, 1], [1, 0, 3, 2], [1, 0, 2, 3], [1, 0, 1, 4], [0, 3, 1, 2], [0, 3, 0, 3], [0, 2, 3, 1], [0, 2, 2, 2], [0, 2, 1, 3], [0, 2, 0, 4], [0, 1, 5, 0], [0, 1, 4, 1], [0, 1, 3, 2], [0, 0, 6, 0], [0, 0, 5, 1], [1, 0, 0, 6], [0, 1, 2, 4], [0, 1, 1, 5], [0, 1, 0, 6], [0, 0, 4, 3], [0, 0, 3, 4], [0, 0, 2, 5], [0, 0, 1, 6], [0, 0, 0, 8]]}'

data = json.loads(data)

large_roll_width = data['large_roll_width']
demands = data['demands']
roll_width_options = data['roll_width_options']
patterns = data['patterns']

# Define the Linear Programming problem
problem = pulp.LpProblem("Minimize_Large_Rolls", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Integer') for i in range(len(patterns))]

# Objective Function
problem += pulp.lpSum(x)

# Constraints
for j in range(len(demands)):
    problem += pulp.lpSum(x[i] * patterns[i][j] for i in range(len(patterns))) >= demands[j]

# Solve the problem
problem.solve()

# Prepare the output
total_large_rolls_used = pulp.value(problem.objective)
result_patterns = [
    {"pattern": patterns[i], "amount": int(x[i].value())}
    for i in range(len(patterns)) if x[i].value() > 0
]

# Print results in specified output format
output = {
    "patterns": result_patterns,
    "total_large_rolls_used": int(total_large_rolls_used)
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
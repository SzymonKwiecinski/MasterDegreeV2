import pulp

# Input data
data = {
    'large_roll_width': 70,
    'demands': [40, 65, 80, 75],
    'roll_width_options': [17, 14, 11, 8.5],
    'patterns': [
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

large_roll_width = data['large_roll_width']
demands = data['demands']
patterns = data['patterns']
num_patterns = len(patterns)
num_roll_types = len(demands)

# Define the problem
problem = pulp.LpProblem("Minimize_Large_Rolls", pulp.LpMinimize)

# Define decision variables
x = [pulp.LpVariable(f'pattern_used_{i}', lowBound=0, cat='Integer') for i in range(num_patterns)]

# Objective function: Minimize the number of large rolls used
problem += pulp.lpSum(x[i] for i in range(num_patterns))

# Constraints: Fulfill the demand for each roll width
for j in range(num_roll_types):
    problem += pulp.lpSum(patterns[i][j] * x[i] for i in range(num_patterns)) >= demands[j]

# Solve the problem
problem.solve()

# Prepare the output data
output_patterns = [{"pattern": patterns[i], "amount": int(x[i].varValue)} for i in range(num_patterns) if x[i].varValue > 0]
total_large_rolls_used = int(pulp.value(problem.objective))

result = {
    "patterns": output_patterns,
    "total_large_rolls_used": total_large_rolls_used
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
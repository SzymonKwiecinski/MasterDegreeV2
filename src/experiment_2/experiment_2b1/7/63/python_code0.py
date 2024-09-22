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

large_roll_width = data['large_roll_width']
demands = data['demands']
patterns = data['patterns']

# Create the LP problem
problem = pulp.LpProblem("Minimize_Large_Rolls", pulp.LpMinimize)

# Decision variables: amount of each pattern used
num_patterns = len(patterns)
pattern_vars = pulp.LpVariable.dicts("Pattern", range(num_patterns), lowBound=0, cat='Integer')

# Objective function: to minimize the total number of large rolls used
problem += pulp.lpSum(pattern_vars[i] for i in range(num_patterns))

# Constraints: meet the demand for each roll width
for j in range(len(demands)):
    problem += pulp.lpSum(pattern_vars[i] * patterns[i][j] for i in range(num_patterns)) >= demands[j]

# Solve the problem
problem.solve()

# Collecting results
total_large_rolls_used = pulp.value(problem.objective)
output_patterns = [
    {
        "pattern": patterns[i],
        "amount": pulp.value(pattern_vars[i])
    }
    for i in range(num_patterns) if pulp.value(pattern_vars[i]) > 0
]

# Output format
output = {
    "patterns": output_patterns,
    "total_large_rolls_used": total_large_rolls_used
}

# Print the output
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
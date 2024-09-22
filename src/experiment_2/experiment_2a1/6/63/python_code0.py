import pulp
import json

# Data
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

# Initialize the problem
problem = pulp.LpProblem("MinimizeLargeRolls", pulp.LpMinimize)

# Variables
pattern_vars = [pulp.LpVariable(f'pattern_{i}', lowBound=0, cat='Integer') for i in range(len(data['patterns']))]

# Objective function
problem += pulp.lpSum(pattern_vars), "TotalLargeRolls"

# Constraints
for j in range(len(data['demands'])):
    problem += (pulp.lpSum(pattern_vars[i] * data['patterns'][i][j] for i in range(len(data['patterns']))) >= data['demands'][j]), f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Preparing the output
patterns_output = [{"pattern": data['patterns'][i], "amount": pattern_vars[i].value()} for i in range(len(data['patterns'])) if pattern_vars[i].value() > 0]
total_large_rolls_used = pulp.value(problem.objective)

output = {
    "patterns": patterns_output,
    "total_large_rolls_used": total_large_rolls_used
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
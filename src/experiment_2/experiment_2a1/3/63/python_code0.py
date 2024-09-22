import pulp
import json

data = {'large_roll_width': 70, 'demands': [40, 65, 80, 75], 'roll_width_options': [17, 14, 11, 8.5], 'patterns': [[4, 0, 0, 0], [3, 1, 0, 0], [3, 0, 1, 0], [2, 2, 0, 0], [3, 0, 0, 2], [2, 1, 2, 0], [2, 1, 1, 1], [2, 1, 0, 2], [2, 0, 3, 0], [2, 0, 2, 1], [2, 0, 1, 2], [1, 3, 1, 0], [1, 3, 0, 1], [1, 2, 2, 0], [1, 2, 1, 1], [1, 2, 0, 2], [1, 1, 3, 0], [0, 5, 0, 0], [0, 4, 1, 0], [0, 4, 0, 1], [0, 3, 2, 0], [2, 0, 0, 4], [1, 1, 2, 2], [1, 1, 1, 3], [1, 1, 0, 4], [1, 0, 4, 1], [1, 0, 3, 2], [1, 0, 2, 3], [1, 0, 1, 4], [0, 3, 1, 2], [0, 3, 0, 3], [0, 2, 3, 1], [0, 2, 2, 2], [0, 2, 1, 3], [0, 2, 0, 4], [0, 1, 5, 0], [0, 1, 4, 1], [0, 1, 3, 2], [0, 0, 6, 0], [0, 0, 5, 1], [1, 0, 0, 6], [0, 1, 2, 4], [0, 1, 1, 5], [0, 1, 0, 6], [0, 0, 4, 3], [0, 0, 3, 4], [0, 0, 2, 5], [0, 0, 1, 6], [0, 0, 0, 8]]}

# Create the LP problem
problem = pulp.LpProblem("MinimizeLargeRolls", pulp.LpMinimize)

# Define variables
N = len(data['patterns'])
x = pulp.LpVariable.dicts("pattern", range(N), lowBound=0, cat='Integer')

# Objective function: Minimize the number of large rolls
problem += pulp.lpSum(x[i] for i in range(N)), "TotalLargeRolls"

# Constraints based on demands
for j in range(len(data['demands'])):
    problem += pulp.lpSum(x[i] * data['patterns'][i][j] for i in range(N)) >= data['demands'][j], f"DemandRollWidth_{j}"

# Solve the problem
problem.solve()

# Prepare output
total_large_rolls = pulp.value(problem.objective)
patterns_used = [
    {"pattern": data['patterns'][i], "amount": int(x[i].varValue)} 
    for i in range(N) if x[i].varValue > 0
]

output = {
    "patterns": patterns_used,
    "total_large_rolls_used": int(total_large_rolls)
}

print(json.dumps(output, indent=2))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
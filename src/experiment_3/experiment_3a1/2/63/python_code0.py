import pulp
import json

# Data
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

# Problem Definition
problem = pulp.LpProblem("PaperCutting", pulp.LpMinimize)

# Parameters
W = data['large_roll_width']
M = len(data['demands'])
N = len(data['patterns'])
demands = data['demands']
patterns = data['patterns']

# Decision Variables
x = pulp.LpVariable.dicts("pattern", range(N), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(x[i] for i in range(N))

# Demand Constraints
for j in range(M):
    problem += pulp.lpSum(patterns[i][j] * x[i] for i in range(N)) >= demands[j]

# Roll Width Constraint
for i in range(N):
    problem += pulp.lpSum(patterns[i][j] * x[i] for j in range(M)) <= W

# Solve the problem
problem.solve()

# Collecting results
results = []
for i in range(N):
    if x[i].varValue > 0:  # Only include patterns that are used
        results.append({
            "pattern": patterns[i],
            "amount": int(x[i].varValue)
        })

# Output
output = {
    "patterns": results,
    "total_large_rolls_used": int(pulp.value(problem.objective))
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
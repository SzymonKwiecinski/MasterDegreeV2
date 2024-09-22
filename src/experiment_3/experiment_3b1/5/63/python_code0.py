import pulp
import json

# Data provided in the problem
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

# Extracting parameters from data
L = data['large_roll_width']
M = len(data['demands'])
N = len(data['patterns'])
demands = data['demands']
patterns = data['patterns']

# Define the problem
problem = pulp.LpProblem("Minimize_Large_Rolls", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat='Integer')

# Objective function: Minimize the total number of large rolls used
problem += pulp.lpSum(x[i] for i in range(N)), "Total_Large_Rolls"

# Constraints for meeting demands
for j in range(M):
    problem += (
        pulp.lpSum(x[i] * patterns[i][j] for i in range(N)) >= demands[j],
        f"Demand_Fulfillment_{j}"
    )

# Solve the problem
problem.solve()

# Output results
patterns_result = []
total_large_rolls = sum(x[i].varValue for i in range(N))

for i in range(N):
    patterns_result.append({
        "pattern": patterns[i],
        "amount": x[i].varValue
    })

output = {
    "patterns": patterns_result,
    "total_large_rolls_used": total_large_rolls
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
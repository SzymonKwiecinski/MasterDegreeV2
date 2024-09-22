import json
import pulp

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

# Create the LP problem
problem = pulp.LpProblem("Paper_Cutting_Problem", pulp.LpMinimize)

# Variables: amount of each pattern used
amounts = [pulp.LpVariable(f'amount_{i}', lowBound=0, cat='Integer') for i in range(len(data['patterns']))]

# Objective Function: Minimize the number of large rolls used
problem += pulp.lpSum(amounts)

# Constraints: meet the demands for each width
for j in range(len(data['demands'])):
    problem += (
        pulp.lpSum(amounts[i] * data['patterns'][i][j] for i in range(len(data['patterns']))) >= data['demands'][j]
    )

# Solve the problem
problem.solve()

# Collect results
patterns_used = []
for i in range(len(data['patterns'])):
    if amounts[i].value() > 0:
        patterns_used.append({
            "pattern": data['patterns'][i],
            "amount": int(amounts[i].value())
        })

total_large_rolls_used = int(pulp.value(problem.objective))

# Output the results
output = {
    "patterns": patterns_used,
    "total_large_rolls_used": total_large_rolls_used
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
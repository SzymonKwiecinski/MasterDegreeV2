import pulp

# Load data
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

# Unpack data
large_roll_width = data['large_roll_width']
demands = data['demands']
patterns = data['patterns']

# Create the linear programming problem
problem = pulp.LpProblem("Minimize_Large_Rolls", pulp.LpMinimize)

# Decision variables
pattern_usage = [pulp.LpVariable(f"pattern_use_{i}", lowBound=0, cat='Integer') for i in range(len(patterns))]

# Objective function: Minimize the number of large rolls used
problem += pulp.lpSum(pattern_usage)

# Constraints: Fulfill demand for each roll width option
for j in range(len(demands)):
    problem += pulp.lpSum(pattern_usage[i] * patterns[i][j] for i in range(len(patterns))) >= demands[j], f"Demand_constraint_{j}"

# Solve the problem
problem.solve()

# Prepare the output
pattern_application = []
for i in range(len(patterns)):
    if pattern_usage[i].varValue > 0:
        pattern_application.append({
            "pattern": patterns[i],
            "amount": int(pattern_usage[i].varValue)
        })

total_large_rolls_used = int(pulp.value(problem.objective))

# Output format
output = {
    "patterns": pattern_application,
    "total_large_rolls_used": total_large_rolls_used
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
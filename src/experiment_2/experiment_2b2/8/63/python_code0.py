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

# Unpack data
large_roll_width = data['large_roll_width']
demands = data['demands']
patterns = data['patterns']

# Create the problem
problem = pulp.LpProblem("Minimize_Large_Rolls", pulp.LpMinimize)

# Variables
num_patterns = len(patterns)
x_vars = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Integer') for i in range(num_patterns)]

# Objective
problem += pulp.lpSum(x_vars)

# Constraints
for j in range(len(demands)):
    problem += pulp.lpSum(patterns[i][j] * x_vars[i] for i in range(num_patterns)) >= demands[j]

# Solve the problem    
problem.solve()

# Output result
results = {"patterns": [], "total_large_rolls_used": pulp.value(problem.objective)}
for i in range(num_patterns):
    if pulp.value(x_vars[i]) > 0:
        results["patterns"].append(
            {"pattern": patterns[i], "amount": int(pulp.value(x_vars[i]))}
        )

print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp

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

# Unpack data
L = data['large_roll_width']
demands = data['demands']
roll_width_options = data['roll_width_options']
patterns = data['patterns']

# Setup the LP problem
problem = pulp.LpProblem("PaperCuttingProblem", pulp.LpMinimize)

# Define decision variables
x_vars = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Integer') for i in range(len(patterns))]

# Objective function
problem += pulp.lpSum(x_vars)

# Demand constraints
for j, demand in enumerate(demands):
    problem += pulp.lpSum(patterns[i][j] * x_vars[i] for i in range(len(patterns))) >= demand

# Width constraints
for i, pattern in enumerate(patterns):
    problem += pulp.lpSum(pattern[j] * roll_width_options[j] for j in range(len(roll_width_options))) <= L

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
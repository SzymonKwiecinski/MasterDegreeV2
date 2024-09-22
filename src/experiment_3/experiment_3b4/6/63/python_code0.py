import pulp

# Data
data = {
    'large_roll_width': 70,
    'demands': [40, 65, 80, 75],
    'roll_width_options': [17, 14, 11, 8.5],
    'patterns': [
        [4, 0, 0, 0], [3, 1, 0, 0], [3, 0, 1, 0],
        [2, 2, 0, 0], [3, 0, 0, 2], [2, 1, 2, 0],
        [2, 1, 1, 1], [2, 1, 0, 2], [2, 0, 3, 0],
        [2, 0, 2, 1], [2, 0, 1, 2], [1, 3, 1, 0],
        [1, 3, 0, 1], [1, 2, 2, 0], [1, 2, 1, 1],
        [1, 2, 0, 2], [1, 1, 3, 0], [0, 5, 0, 0],
        [0, 4, 1, 0], [0, 4, 0, 1], [0, 3, 2, 0],
        [2, 0, 0, 4], [1, 1, 2, 2], [1, 1, 1, 3],
        [1, 1, 0, 4], [1, 0, 4, 1], [1, 0, 3, 2],
        [1, 0, 2, 3], [1, 0, 1, 4], [0, 3, 1, 2],
        [0, 3, 0, 3], [0, 2, 3, 1], [0, 2, 2, 2],
        [0, 2, 1, 3], [0, 2, 0, 4], [0, 1, 5, 0],
        [0, 1, 4, 1], [0, 1, 3, 2], [0, 0, 6, 0],
        [0, 0, 5, 1], [1, 0, 0, 6], [0, 1, 2, 4],
        [0, 1, 1, 5], [0, 1, 0, 6], [0, 0, 4, 3],
        [0, 0, 3, 4], [0, 0, 2, 5], [0, 0, 1, 6],
        [0, 0, 0, 8]
    ]
}

# Constants
W = data['large_roll_width']
demands = data['demands']
widths = data['roll_width_options']
patterns = data['patterns']
M = len(widths)
N = len(patterns)

# Problem definition
problem = pulp.LpProblem("Roll_Cutting_Optimization", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Integer') for i in range(N)]
z = pulp.LpVariable("z", lowBound=0, cat='Integer')

# Objective
problem += z

# Constraints
# Demand fulfillment for each roll width
for j in range(M):
    problem += pulp.lpSum(patterns[i][j] * x[i] for i in range(N)) >= demands[j]

# Pattern width constraint
for i in range(N):
    problem += pulp.lpSum(widths[j] * patterns[i][j] for j in range(M)) <= W

# Define total large rolls used
problem += z == pulp.lpSum(x[i] for i in range(N))

# Solve problem
problem.solve()

# Objective and variable values
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
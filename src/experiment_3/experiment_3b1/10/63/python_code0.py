import pulp
import json

# Data from the provided JSON
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

# Initialization of the problem
problem = pulp.LpProblem("Paper_Cutting_Problem", pulp.LpMinimize)

# Indices
N = len(data['patterns'])  # Number of cutting patterns
M = len(data['demands'])    # Number of widths of smaller rolls

# Decision variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(x[i] for i in range(N)), "Minimize_Cutting_Patterns"

# Constraints
# Demand constraints
for j in range(M):
    problem += pulp.lpSum(x[i] * data['patterns'][i][j] for i in range(N)) >= data['demands'][j], f"Demand_Constraint_{j + 1}"

# Width constraints
for i in range(N):
    problem += pulp.lpSum(data['patterns'][i][j] for j in range(M)) <= data['large_roll_width'], f"Width_Constraint_{i + 1}"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
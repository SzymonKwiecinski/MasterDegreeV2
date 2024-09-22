import pulp
import json

# Load the data from the JSON format
data = json.loads('{"large_roll_width": 70, "demands": [40, 65, 80, 75], "roll_width_options": [17, 14, 11, 8.5], "patterns": [[4, 0, 0, 0], [3, 1, 0, 0], [3, 0, 1, 0], [2, 2, 0, 0], [3, 0, 0, 2], [2, 1, 2, 0], [2, 1, 1, 1], [2, 1, 0, 2], [2, 0, 3, 0], [2, 0, 2, 1], [2, 0, 1, 2], [1, 3, 1, 0], [1, 3, 0, 1], [1, 2, 2, 0], [1, 2, 1, 1], [1, 2, 0, 2], [1, 1, 3, 0], [0, 5, 0, 0], [0, 4, 1, 0], [0, 4, 0, 1], [0, 3, 2, 0], [2, 0, 0, 4], [1, 1, 2, 2], [1, 1, 1, 3], [1, 1, 0, 4], [1, 0, 4, 1], [1, 0, 3, 2], [1, 0, 2, 3], [1, 0, 1, 4], [0, 3, 1, 2], [0, 3, 0, 3], [0, 2, 3, 1], [0, 2, 2, 2], [0, 2, 1, 3], [0, 2, 0, 4], [0, 1, 5, 0], [0, 1, 4, 1], [0, 1, 3, 2], [0, 0, 6, 0], [0, 0, 5, 1], [1, 0, 0, 6], [0, 1, 2, 4], [0, 1, 1, 5], [0, 1, 0, 6], [0, 0, 4, 3], [0, 0, 3, 4], [0, 0, 2, 5], [0, 0, 1, 6], [0, 0, 0, 8]]}')

# Parameters
W = data['large_roll_width']
demands = data['demands']
patterns = data['patterns']
N = len(patterns)
M = len(demands)

# Create the problem
problem = pulp.LpProblem("PaperCutting", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("use_pattern", range(N), lowBound=0, cat='Integer')

# Objective Function
problem += pulp.lpSum(x[i] for i in range(N)), "Total Rolls Used"

# Demand satisfaction constraints
for j in range(M):
    problem += (pulp.lpSum(patterns[i][j] * x[i] for i in range(N)) >= demands[j]), f"Demand_Satisfaction_{j}"

# Width constraints
for i in range(N):
    problem += (pulp.lpSum(patterns[i][j] for j in range(M)) <= W * x[i]), f"Width_Constraint_{i}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
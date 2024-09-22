import pulp
import json

# Input data in JSON format
data = json.loads('{"large_roll_width": 70, "demands": [40, 65, 80, 75], "roll_width_options": [17, 14, 11, 8.5], "patterns": [[4, 0, 0, 0], [3, 1, 0, 0], [3, 0, 1, 0], [2, 2, 0, 0], [3, 0, 0, 2], [2, 1, 2, 0], [2, 1, 1, 1], [2, 1, 0, 2], [2, 0, 3, 0], [2, 0, 2, 1], [2, 0, 1, 2], [1, 3, 1, 0], [1, 3, 0, 1], [1, 2, 2, 0], [1, 2, 1, 1], [1, 2, 0, 2], [1, 1, 3, 0], [0, 5, 0, 0], [0, 4, 1, 0], [0, 4, 0, 1], [0, 3, 2, 0], [2, 0, 0, 4], [1, 1, 2, 2], [1, 1, 1, 3], [1, 1, 0, 4], [1, 0, 4, 1], [1, 0, 3, 2], [1, 0, 2, 3], [1, 0, 1, 4], [0, 3, 1, 2], [0, 3, 0, 3], [0, 2, 3, 1], [0, 2, 2, 2], [0, 2, 1, 3], [0, 2, 0, 4], [0, 1, 5, 0], [0, 1, 4, 1], [0, 1, 3, 2], [0, 0, 6, 0], [0, 0, 5, 1], [1, 0, 0, 6], [0, 1, 2, 4], [0, 1, 1, 5], [0, 1, 0, 6], [0, 0, 4, 3], [0, 0, 3, 4], [0, 0, 2, 5], [0, 0, 1, 6], [0, 0, 0, 8]]}')

# Parameters
large_roll_width = data["large_roll_width"]
demands = data["demands"]
patterns = data["patterns"]

# Number of different small roll types and cutting patterns
M = len(demands)
N = len(patterns)

# Initialize the problem
problem = pulp.LpProblem("Paper_Cutting_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum([x[i] for i in range(N)])

# Constraints: demand satisfaction for each small roll type
for j in range(M):
    problem += pulp.lpSum([patterns[i][j] * x[i] for i in range(N)]) >= demands[j]

# Solve the problem
problem.solve()

# Output results
for i in range(N):
    print(f'Pattern {i + 1}: {patterns[i]}, Rolls used: {x[i].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp

# Data
data = {'large_roll_width': 70, 'demands': [40, 65, 80, 75], 'roll_width_options': [17, 14, 11, 8.5], 'patterns': [[4, 0, 0, 0], [3, 1, 0, 0], [3, 0, 1, 0], [2, 2, 0, 0], [3, 0, 0, 2], [2, 1, 2, 0], [2, 1, 1, 1], [2, 1, 0, 2], [2, 0, 3, 0], [2, 0, 2, 1], [2, 0, 1, 2], [1, 3, 1, 0], [1, 3, 0, 1], [1, 2, 2, 0], [1, 2, 1, 1], [1, 2, 0, 2], [1, 1, 3, 0], [0, 5, 0, 0], [0, 4, 1, 0], [0, 4, 0, 1], [0, 3, 2, 0], [2, 0, 0, 4], [1, 1, 2, 2], [1, 1, 1, 3], [1, 1, 0, 4], [1, 0, 4, 1], [1, 0, 3, 2], [1, 0, 2, 3], [1, 0, 1, 4], [0, 3, 1, 2], [0, 3, 0, 3], [0, 2, 3, 1], [0, 2, 2, 2], [0, 2, 1, 3], [0, 2, 0, 4], [0, 1, 5, 0], [0, 1, 4, 1], [0, 1, 3, 2], [0, 0, 6, 0], [0, 0, 5, 1], [1, 0, 0, 6], [0, 1, 2, 4], [0, 1, 1, 5], [0, 1, 0, 6], [0, 0, 4, 3], [0, 0, 3, 4], [0, 0, 2, 5], [0, 0, 1, 6], [0, 0, 0, 8]]}
large_roll_width = data['large_roll_width']
demands = data['demands']
patterns = data['patterns']
M = len(demands)
N = len(patterns)

# Problem
problem = pulp.LpProblem("PaperRollCutting", pulp.LpMinimize)

# Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Integer') for i in range(N)]

# Objective
problem += pulp.lpSum(x), "Minimize_Number_of_Large_Rolls"

# Constraints
for j in range(M):
    problem += pulp.lpSum(patterns[i][j] * x[i] for i in range(N)) >= demands[j], f"Demand_constraint_for_roll_width_{j}"

# Solve
problem.solve()

# Output
solution = {"patterns": [], "total_large_rolls_used": int(pulp.value(problem.objective))}
for i in range(N):
    if x[i].varValue > 0:
        solution["patterns"].append({"pattern": patterns[i], "amount": int(x[i].varValue)})

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
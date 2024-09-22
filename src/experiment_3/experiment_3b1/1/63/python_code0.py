import pulp
import json

# Input data
data = json.loads('{"large_roll_width": 70, "demands": [40, 65, 80, 75], "roll_width_options": [17, 14, 11, 8.5], "patterns": [[4, 0, 0, 0], [3, 1, 0, 0], [3, 0, 1, 0], [2, 2, 0, 0], [3, 0, 0, 2], [2, 1, 2, 0], [2, 1, 1, 1], [2, 1, 0, 2], [2, 0, 3, 0], [2, 0, 2, 1], [2, 0, 1, 2], [1, 3, 1, 0], [1, 3, 0, 1], [1, 2, 2, 0], [1, 2, 1, 1], [1, 2, 0, 2], [1, 1, 3, 0], [0, 5, 0, 0], [0, 4, 1, 0], [0, 4, 0, 1], [0, 3, 2, 0], [2, 0, 0, 4], [1, 1, 2, 2], [1, 1, 1, 3], [1, 1, 0, 4], [1, 0, 4, 1], [1, 0, 3, 2], [1, 0, 2, 3], [1, 0, 1, 4], [0, 3, 1, 2], [0, 3, 0, 3], [0, 2, 3, 1], [0, 2, 2, 2], [0, 2, 1, 3], [0, 2, 0, 4], [0, 1, 5, 0], [0, 1, 4, 1], [0, 1, 3, 2], [0, 0, 6, 0], [0, 0, 5, 1], [1, 0, 0, 6], [0, 1, 2, 4], [0, 1, 1, 5], [0, 1, 0, 6], [0, 0, 4, 3], [0, 0, 3, 4], [0, 0, 2, 5], [0, 0, 1, 6], [0, 0, 0, 8]]}')

# Parameters
L = data['large_roll_width']
demands = data['demands']
patterns = data['patterns']

M = len(demands)
N = len(patterns)

# Create the LP problem
problem = pulp.LpProblem("Paper_Cutting_Problem", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(N)]

# Objective Function
problem += pulp.lpSum(x[i] for i in range(N))

# Constraints
for j in range(M):
    problem += pulp.lpSum(patterns[i][j] * x[i] for i in range(N)) >= demands[j], f"Demand_Constraint_{j+1}"

for i in range(N):
    problem += pulp.lpSum(patterns[i][j] for j in range(M)) <= L, f"Cutting_Pattern_Constraint_{i+1}"

# Solve the problem
problem.solve()

# Output the results
patterns_used = [(i, x[i].varValue) for i in range(N) if x[i].varValue > 0]
total_large_rolls_used = sum(x[i].varValue for i in range(N))

print(f'Patterns used and their amounts: {patterns_used}')
print(f'Total large rolls used: {total_large_rolls_used}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
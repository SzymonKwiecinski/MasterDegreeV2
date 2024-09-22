import pulp
import json

data = {'large_roll_width': 70, 'demands': [40, 65, 80, 75], 'roll_width_options': [17, 14, 11, 8.5], 'patterns': [[4, 0, 0, 0], [3, 1, 0, 0], [3, 0, 1, 0], [2, 2, 0, 0], [3, 0, 0, 2], [2, 1, 2, 0], [2, 1, 1, 1], [2, 1, 0, 2], [2, 0, 3, 0], [2, 0, 2, 1], [2, 0, 1, 2], [1, 3, 1, 0], [1, 3, 0, 1], [1, 2, 2, 0], [1, 2, 1, 1], [1, 2, 0, 2], [1, 1, 3, 0], [0, 5, 0, 0], [0, 4, 1, 0], [0, 4, 0, 1], [0, 3, 2, 0], [2, 0, 0, 4], [1, 1, 2, 2], [1, 1, 1, 3], [1, 1, 0, 4], [1, 0, 4, 1], [1, 0, 3, 2], [1, 0, 2, 3], [1, 0, 1, 4], [0, 3, 1, 2], [0, 3, 0, 3], [0, 2, 3, 1], [0, 2, 2, 2], [0, 2, 1, 3], [0, 2, 0, 4], [0, 1, 5, 0], [0, 1, 4, 1], [0, 1, 3, 2], [0, 0, 6, 0], [0, 0, 5, 1], [1, 0, 0, 6], [0, 1, 2, 4], [0, 1, 1, 5], [0, 1, 0, 6], [0, 0, 4, 3], [0, 0, 3, 4], [0, 0, 2, 5], [0, 0, 1, 6], [0, 0, 0, 8]]}

large_roll_width = data['large_roll_width']
demands = data['demands']
patterns = data['patterns']

# Create a linear programming problem
problem = pulp.LpProblem("Paper_Production", pulp.LpMinimize)

# Decision variables for the number of large rolls used with each pattern
pattern_vars = pulp.LpVariable.dicts("Pattern", range(len(patterns)), lowBound=0, cat='Integer')

# Objective function: Minimize the total number of large rolls used
problem += pulp.lpSum(pattern_vars[i] for i in range(len(patterns)))

# Constraints to meet the demands
for j in range(len(demands)):
    problem += pulp.lpSum(pattern_vars[i] * patterns[i][j] for i in range(len(patterns))) >= demands[j], f"Demand_{j}"

# Solve the problem
problem.solve()

# Prepare output
solution = {
    "patterns": [{"pattern": [patterns[i][j] for j in range(len(demands))], "amount": int(pattern_vars[i].value())} for i in range(len(patterns)) if pattern_vars[i].value() > 0],
    "total_large_rolls_used": int(pulp.value(problem.objective))
}

print(json.dumps(solution, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
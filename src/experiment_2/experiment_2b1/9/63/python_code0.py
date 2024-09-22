import json
import pulp

# Input data
data = {'large_roll_width': 70, 'demands': [40, 65, 80, 75], 'roll_width_options': [17, 14, 11, 8.5], 
        'patterns': [[4, 0, 0, 0], [3, 1, 0, 0], [3, 0, 1, 0], [2, 2, 0, 0], [3, 0, 0, 2], 
                     [2, 1, 2, 0], [2, 1, 1, 1], [2, 1, 0, 2], [2, 0, 3, 0], [2, 0, 2, 1], 
                     [2, 0, 1, 2], [1, 3, 1, 0], [1, 3, 0, 1], [1, 2, 2, 0], [1, 2, 1, 1], 
                     [1, 2, 0, 2], [1, 1, 3, 0], [0, 5, 0, 0], [0, 4, 1, 0], [0, 4, 0, 1], 
                     [0, 3, 2, 0], [2, 0, 0, 4], [1, 1, 2, 2], [1, 1, 1, 3], [1, 1, 0, 4], 
                     [1, 0, 4, 1], [1, 0, 3, 2], [1, 0, 2, 3], [1, 0, 1, 4], [0, 3, 1, 2], 
                     [0, 3, 0, 3], [0, 2, 3, 1], [0, 2, 2, 2], [0, 2, 1, 3], [0, 2, 0, 4], 
                     [0, 1, 5, 0], [0, 1, 4, 1], [0, 1, 3, 2], [0, 0, 6, 0], [0, 0, 5, 1], 
                     [1, 0, 0, 6], [0, 1, 2, 4], [0, 1, 1, 5], [0, 1, 0, 6], [0, 0, 4, 3], 
                     [0, 0, 3, 4], [0, 0, 2, 5], [0, 0, 1, 6], [0, 0, 0, 8]]}

large_roll_width = data['large_roll_width']
demands = data['demands']
patterns = data['patterns']

# Problem setup
problem = pulp.LpProblem("Paper_Cutting_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(len(patterns)), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(x[i] for i in range(len(patterns))), "Minimize_Large_Rolls"

# Constraints
for j in range(len(demands)):
    problem += (pulp.lpSum(patterns[i][j] * x[i] for i in range(len(patterns))) >= demands[j]), f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Output results
total_large_rolls_used = pulp.value(problem.objective)
output_patterns = [{"pattern": patterns[i], "amount": x[i].varValue} for i in range(len(patterns)) if x[i].varValue > 0]

results = {
    "patterns": output_patterns,
    "total_large_rolls_used": total_large_rolls_used
}

print(json.dumps(results, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
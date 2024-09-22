import pulp
import json

data = {'large_roll_width': 70, 'demands': [40, 65, 80, 75], 
        'roll_width_options': [17, 14, 11, 8.5], 
        'patterns': [[4, 0, 0, 0], [3, 1, 0, 0], [3, 0, 1, 0], [2, 2, 0, 0], 
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
                     [0, 0, 0, 8]]}

large_roll_width = data['large_roll_width']
demands = data['demands']
patterns = data['patterns']

# Create the LP problem
problem = pulp.LpProblem("Minimize_Large_Rolls_Used", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("pattern", range(len(patterns)), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(x[i] for i in range(len(patterns)))

# Constraints
for j in range(len(demands)):
    problem += pulp.lpSum(patterns[i][j] * x[i] for i in range(len(patterns))) >= demands[j], f"Demand_Constraint_{j}"

# Solve the problem
problem.solve()

# Collecting the output
total_large_rolls_used = pulp.value(problem.objective)
patterns_used = [{"pattern": patterns[i], "amount": int(x[i].value())} for i in range(len(patterns)) if x[i].value() > 0]

output = {
    "patterns": patterns_used,
    "total_large_rolls_used": int(total_large_rolls_used)
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_large_rolls_used}</OBJ>')
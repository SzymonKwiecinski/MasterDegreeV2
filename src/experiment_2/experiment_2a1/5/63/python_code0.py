import pulp
import json

# Input data
data = {
    'large_roll_width': 70,
    'demands': [40, 65, 80, 75],
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
                 [0, 0, 0, 8]]
}

# Parameters
M = len(data['demands'])
N = len(data['patterns'])
demand = data['demands']
patterns = data['patterns']

# Create the model
problem = pulp.LpProblem("Minimize_Large_Rolls_Used", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("pattern", range(N), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(x[i] for i in range(N)), "Total_Large_Rolls_Used"

# Constraints
for j in range(M):
    problem += pulp.lpSum(x[i] * patterns[i][j] for i in range(N)) >= demand[j], f"Demand_Constraint_for_Width_{j}"

# Solve the problem
problem.solve()

# Prepare the output
patterns_used = [{"pattern": patterns[i], "amount": int(x[i].varValue)} for i in range(N) if x[i].varValue > 0]
total_large_rolls_used = int(pulp.value(problem.objective))

# Final output format
output = {
    "patterns": patterns_used,
    "total_large_rolls_used": total_large_rolls_used
}

# Print the output and the objective value
print(json.dumps(output, indent=4))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
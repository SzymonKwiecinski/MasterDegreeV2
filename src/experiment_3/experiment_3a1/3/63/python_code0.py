import pulp
import json

# Data provided in JSON format
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

# Parameters extraction
demands = data['demands']
patterns = data['patterns']

# Number of different types of smaller rolls
M = len(demands)
# Number of cutting patterns available
N = len(patterns)

# Create the linear programming problem
problem = pulp.LpProblem("Paper_Cutting_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(x[i] for i in range(N)), "Total_Large_Rolls_Used"

# Demand constraints for each smaller roll width j
for j in range(M):
    problem += pulp.lpSum(patterns[i][j] * x[i] for i in range(N)) >= demands[j], f"Demand_Constraint_{j+1}"

# Solve the problem
problem.solve()

# Output the results
patterns_used = [
    {"pattern": patterns[i], "amount": x[i].varValue} 
    for i in range(N) if x[i].varValue > 0
]

total_large_rolls_used = pulp.value(problem.objective)

# Print the objective value
print(f' (Objective Value): <OBJ>{total_large_rolls_used}</OBJ>')

# Print patterns used
print(json.dumps({"patterns": patterns_used, "total_large_rolls_used": total_large_rolls_used}, indent=4))
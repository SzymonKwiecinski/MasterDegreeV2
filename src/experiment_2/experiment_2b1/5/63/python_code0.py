import json
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpBinary, LpStatus, value

# Load the data from the given format
data = {
    'large_roll_width': 70, 
    'demands': [40, 65, 80, 75], 
    'roll_width_options': [17, 14, 11, 8.5], 
    'patterns': [[4, 0, 0, 0], [3, 1, 0, 0], [3, 0, 1, 0], [2, 2, 0, 0], [3, 0, 0, 2], 
                 [2, 1, 2, 0], [2, 1, 1, 1], [2, 1, 0, 2], [2, 0, 3, 0], [2, 0, 2, 1], 
                 [2, 0, 1, 2], [1, 3, 1, 0], [1, 3, 0, 1], [1, 2, 2, 0], [1, 2, 1, 1], 
                 [1, 2, 0, 2], [1, 1, 3, 0], [0, 5, 0, 0], [0, 4, 1, 0], [0, 4, 0, 1], 
                 [0, 3, 2, 0], [2, 0, 0, 4], [1, 1, 2, 2], [1, 1, 1, 3], [1, 1, 0, 4], 
                 [1, 0, 4, 1], [1, 0, 3, 2], [1, 0, 2, 3], [1, 0, 1, 4], [0, 3, 1, 2], 
                 [0, 3, 0, 3], [0, 2, 3, 1], [0, 2, 2, 2], [0, 2, 1, 3], [0, 2, 0, 4], 
                 [0, 1, 5, 0], [0, 1, 4, 1], [0, 1, 3, 2], [0, 0, 6, 0], [0, 0, 5, 1], 
                 [1, 0, 0, 6], [0, 1, 2, 4], [0, 1, 1, 5], [0, 1, 0, 6], [0, 0, 4, 3], 
                 [0, 0, 3, 4], [0, 0, 2, 5], [0, 0, 1, 6], [0, 0, 0, 8]]
}

large_roll_width = data['large_roll_width']
demands = data['demands']
patterns = data['patterns']

# Number of smaller rolls types and cutting patterns
M = len(demands)
N = len(patterns)

# Initialize the problem
problem = LpProblem("Minimize_Large_Rolls", LpMinimize)

# Decision variables for the amount of each cutting pattern used
amounts = [LpVariable(f'amount_{i}', lowBound=0, cat=LpInteger) for i in range(N)]

# Objective function: Minimize the total number of large rolls used
problem += lpSum(amounts)

# Constraints for each roll width based on the demands
for j in range(M):
    problem += lpSum(amounts[i] * patterns[i][j] for i in range(N)) >= demands[j]

# Solve the problem
problem.solve()

# Output the results
patterns_used = [{"pattern": patterns[i], "amount": amounts[i].varValue} for i in range(N) if amounts[i].varValue > 0]
total_large_rolls_used = value(problem.objective)

output = {
    "patterns": patterns_used,
    "total_large_rolls_used": total_large_rolls_used
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
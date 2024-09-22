import json
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpInteger, value

# Input data in JSON format
data = {'large_roll_width': 70, 'demands': [40, 65, 80, 75], 
        'roll_width_options': [17, 14, 11, 8.5], 
        'patterns': [[4, 0, 0, 0], [3, 1, 0, 0], [3, 0, 1, 0], 
                     [2, 2, 0, 0], [3, 0, 0, 2], [2, 1, 2, 0], 
                     [2, 1, 1, 1], [2, 1, 0, 2], [2, 0, 3, 0], 
                     [2, 0, 2, 1], [2, 0, 1, 2], [1, 3, 1, 0], 
                     [1, 3, 0, 1], [1, 2, 2, 0], [1, 2, 1, 1], 
                     [1, 2, 0, 2], [1, 1, 3, 0], [0, 5, 0, 0], 
                     [0, 4, 1, 0], [0, 4, 0, 1], [0, 3, 2, 0], 
                     [2, 0, 0, 4], [1, 1, 2, 2], [1, 1, 1, 3], 
                     [1, 1, 0, 4], [1, 0, 4, 1], [1, 0, 3, 2], 
                     [1, 0, 2, 3], [1, 0, 1, 4], [0, 3, 1, 2], 
                     [0, 3, 0, 3], [0, 2, 3, 1], [0, 2, 2, 2], 
                     [0, 2, 1, 3], [0, 2, 0, 4], [0, 1, 5, 0], 
                     [0, 1, 4, 1], [0, 1, 3, 2], [0, 0, 6, 0], 
                     [0, 0, 5, 1], [1, 0, 0, 6], [0, 1, 2, 4], 
                     [0, 1, 1, 5], [0, 1, 0, 6], [0, 0, 4, 3], 
                     [0, 0, 3, 4], [0, 0, 2, 5], [0, 0, 1, 6], 
                     [0, 0, 0, 8]]}

# Extracting parameters
large_roll_width = data['large_roll_width']
demands = data['demands']
patterns = data['patterns']

# Number of patterns and roll widths
num_patterns = len(patterns)
num_rolls = len(demands)

# Define the problem
problem = LpProblem("PaperCuttingProblem", LpMinimize)

# Define decision variables for the number of times each cutting pattern is used
pattern_vars = LpVariable.dicts("Pattern", range(num_patterns), lowBound=0, cat=LpInteger)

# Objective function: Minimize the total number of large rolls used
problem += lpSum(pattern_vars[i] for i in range(num_patterns))

# Constraints: Ensure that demand for each roll is met
for j in range(num_rolls):
    problem += lpSum(patterns[i][j] * pattern_vars[i] for i in range(num_patterns)) >= demands[j]

# Solve the problem
problem.solve()

# Prepare output
total_large_rolls_used = value(problem.objective)
output = {
    "patterns": [{"pattern": patterns[i], "amount": pattern_vars[i].varValue} for i in range(num_patterns)],
    "total_large_rolls_used": total_large_rolls_used
}

# Print output
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')
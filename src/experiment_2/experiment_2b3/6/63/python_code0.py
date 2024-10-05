from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value
import json

# Load data
data = json.loads('{"large_roll_width": 70, "demands": [40, 65, 80, 75], "roll_width_options": [17, 14, 11, 8.5], "patterns": [[4, 0, 0, 0], [3, 1, 0, 0], [3, 0, 1, 0], [2, 2, 0, 0], [3, 0, 0, 2], [2, 1, 2, 0], [2, 1, 1, 1], [2, 1, 0, 2], [2, 0, 3, 0], [2, 0, 2, 1], [2, 0, 1, 2], [1, 3, 1, 0], [1, 3, 0, 1], [1, 2, 2, 0], [1, 2, 1, 1], [1, 2, 0, 2], [1, 1, 3, 0], [0, 5, 0, 0], [0, 4, 1, 0], [0, 4, 0, 1], [0, 3, 2, 0], [2, 0, 0, 4], [1, 1, 2, 2], [1, 1, 1, 3], [1, 1, 0, 4], [1, 0, 4, 1], [1, 0, 3, 2], [1, 0, 2, 3], [1, 0, 1, 4], [0, 3, 1, 2], [0, 3, 0, 3], [0, 2, 3, 1], [0, 2, 2, 2], [0, 2, 1, 3], [0, 2, 0, 4], [0, 1, 5, 0], [0, 1, 4, 1], [0, 1, 3, 2], [0, 0, 6, 0], [0, 0, 5, 1], [1, 0, 0, 6], [0, 1, 2, 4], [0, 1, 1, 5], [0, 1, 0, 6], [0, 0, 4, 3], [0, 0, 3, 4], [0, 0, 2, 5], [0, 0, 1, 6], [0, 0, 0, 8]]}')

large_roll_width = data['large_roll_width']
demands = data['demands']
patterns = data['patterns']

M = len(demands)
N = len(patterns)

# Initialize the linear programming problem
problem = LpProblem("Minimize_Large_Rolls", LpMinimize)

# Create decision variables for the number of times each pattern is used
x = LpVariable.dicts("pattern", range(N), lowBound=0, cat='Integer')

# Objective function: Minimize the total number of large rolls used
problem += lpSum(x[i] for i in range(N))

# Constraints: Fulfill the demand for each type of smaller roll
for j in range(M):
    problem += lpSum(patterns[i][j] * x[i] for i in range(N)) >= demands[j]

# Solve the problem
problem.solve()

# Collect the results
solution = {
    "patterns": [{"pattern": patterns[i], "amount": x[i].varValue} for i in range(N) if x[i].varValue > 0],
    "total_large_rolls_used": value(problem.objective)
}

output_json = json.dumps(solution, indent=2)
print(output_json)
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')
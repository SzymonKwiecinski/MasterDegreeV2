from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value, LpInteger

# Input data
data = {
    "large_roll_width": 70,
    "roll_width_options": [17, 14, 11, 8.5],
    "demands": [40, 65, 80, 75],
    "patterns": [
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

# Constants
M = len(data['demands'])  # Number of small roll types
N = len(data['patterns'])  # Number of available patterns

# Define the MILP problem
problem = LpProblem("Paper_Production", LpMinimize)

# Decision variables: number of times each pattern is used
x = LpVariable.dicts("Pattern", range(N), lowBound=0, cat=LpInteger)

# Objective: Minimize the total number of large rolls used
problem += lpSum(x[i] for i in range(N))

# Constraints: Meet the demand for each roll type
for j in range(M):
    problem += lpSum(data['patterns'][i][j] * x[i] for i in range(N)) >= data['demands'][j]

# Solve the problem
problem.solve()

# Build the output data
solution = {
    "patterns": [
        {
            "pattern": data['patterns'][i],
            "amount": int(value(x[i]))
        }
        for i in range(N) if value(x[i]) > 0
    ],
    "total_large_rolls_used": int(value(problem.objective))
}

# Print the solution
print(solution)
print(f'(Objective Value): <OBJ>{value(problem.objective)}</OBJ>')
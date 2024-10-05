import pulp

# Extract data from the provided JSON
data = {
    'large_roll_width': 70,
    'demands': [40, 65, 80, 75],
    'roll_width_options': [17, 14, 11, 8.5],
    'patterns': [
        [4, 0, 0, 0],
        [3, 1, 0, 0],
        [3, 0, 1, 0],
        [2, 2, 0, 0],
        [3, 0, 0, 2],
        [2, 1, 2, 0],
        [2, 1, 1, 1],
        [2, 1, 0, 2],
        [2, 0, 3, 0],
        [2, 0, 2, 1],
        [2, 0, 1, 2],
        [1, 3, 1, 0],
        [1, 3, 0, 1],
        [1, 2, 2, 0],
        [1, 2, 1, 1],
        [1, 2, 0, 2],
        [1, 1, 3, 0],
        [0, 5, 0, 0],
        [0, 4, 1, 0],
        [0, 4, 0, 1],
        [0, 3, 2, 0],
        [2, 0, 0, 4],
        [1, 1, 2, 2],
        [1, 1, 1, 3],
        [1, 1, 0, 4],
        [1, 0, 4, 1],
        [1, 0, 3, 2],
        [1, 0, 2, 3],
        [1, 0, 1, 4],
        [0, 3, 1, 2],
        [0, 3, 0, 3],
        [0, 2, 3, 1],
        [0, 2, 2, 2],
        [0, 2, 1, 3],
        [0, 2, 0, 4],
        [0, 1, 5, 0],
        [0, 1, 4, 1],
        [0, 1, 3, 2],
        [0, 0, 6, 0],
        [0, 0, 5, 1],
        [1, 0, 0, 6],
        [0, 1, 2, 4],
        [0, 1, 1, 5],
        [0, 1, 0, 6],
        [0, 0, 4, 3],
        [0, 0, 3, 4],
        [0, 0, 2, 5],
        [0, 0, 1, 6],
        [0, 0, 0, 8]
    ]
}

# Define the problem
problem = pulp.LpProblem("Minimize_Large_Rolls", pulp.LpMinimize)

# Number of patterns and number of roll types
N = len(data['patterns'])
M = len(data['demands'])

# Decision variables: number of times each pattern is used
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat=pulp.LpInteger) for i in range(N)]

# Objective function: Minimize the total number of large rolls used
problem += pulp.lpSum(x[i] for i in range(N))

# Constraints: Demand for each type of small rolls must be satisfied
for j in range(M):
    problem += pulp.lpSum(data['patterns'][i][j] * x[i] for i in range(N)) >= data['demands'][j]

# Solve the problem
problem.solve()

# Extract the results
total_large_rolls = sum([pulp.value(x[i]) for i in range(N)])
patterns_result = [{"pattern": data['patterns'][i], "amount": int(pulp.value(x[i]))} for i in range(N) if pulp.value(x[i]) > 0]

# Output the result
result = {
    "patterns": patterns_result,
    "total_large_rolls_used": total_large_rolls
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp

# Data from JSON
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

M = len(data['demands'])
N = len(data['patterns'])

# Create the problem instance
problem = pulp.LpProblem("PaperCuttingProblem", pulp.LpMinimize)

# Decision variables: x_i is the number of times pattern i is used
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Integer') for i in range(N)]

# Objective function: Minimize the total number of large rolls used
problem += pulp.lpSum(x[i] for i in range(N))

# Constraints: Meet the demand for each roll width
for j in range(M):
    problem += pulp.lpSum(data['patterns'][i][j] * x[i] for i in range(N)) >= data['demands'][j]

# Solve the problem
problem.solve()

# Output the results
print(f'Total Large Rolls Used: {pulp.value(problem.objective)}')
for i in range(N):
    if x[i].varValue and x[i].varValue > 0:
        print(f'Pattern {i+1} used {x[i].varValue} times: {data["patterns"][i]}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
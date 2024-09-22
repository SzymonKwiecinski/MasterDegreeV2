import pulp

# Data input
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}

N = data['N']
Distances = data['Distances']
start_city = data['StartCity']

# Problem definition
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts('x', ((i, j) for i in range(N) for j in range(N)), cat='Binary')
u = pulp.LpVariable.dicts('u', (i for i in range(N)), lowBound=1, cat='Continuous')

# Objective function
problem += pulp.lpSum(Distances[i][j] * x[i, j] for i in range(N) for j in range(N))

# Constraints
# Depart from each city once
for i in range(N):
    problem += pulp.lpSum(x[i, j] for j in range(N) if j != i) == 1

# Arrive at each city once
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(N) if i != j) == 1

# Subtour elimination (MTZ constraints)
u[start_city] = 1

for i in range(1, N):
    problem += u[i] >= 2
    problem += u[i] <= N

for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + N * x[i, j] <= N - 1

# Solving the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
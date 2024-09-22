import pulp

# Data
data = {
    'N': 6,
    'Distances': [
        [0, 182, 70, 399, 56, 214],
        [182, 0, 255, 229, 132, 267],
        [70, 255, 0, 472, 127, 287],
        [399, 229, 472, 0, 356, 484],
        [56, 132, 127, 356, 0, 179],
        [214, 267, 287, 484, 179, 0]
    ],
    'StartCity': 0
}

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Problem
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Variables
x = {(i, j): pulp.LpVariable(f'x_{i}_{j}', cat='Binary') for i in range(N) for j in range(N) if i != j}
u = {i: pulp.LpVariable(f'u_{i}', lowBound=1, upBound=N-1, cat='Continuous') for i in range(1, N)}

# Objective
problem += pulp.lpSum(distances[i][j] * x[i, j] for i in range(N) for j in range(N) if i != j)

# Constraints
for i in range(N):
    if i != start_city:
        problem += pulp.lpSum(x[i, j] for j in range(N) if i != j) == 1

for j in range(N):
    if j != start_city:
        problem += pulp.lpSum(x[i, j] for i in range(N) if i != j) == 1

problem += pulp.lpSum(x[start_city, j] for j in range(1, N)) == 1
problem += pulp.lpSum(x[i, start_city] for i in range(1, N)) == 1

for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + (N - 1) * x[i, j] <= N - 2

# Solve
problem.solve()

# Output objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
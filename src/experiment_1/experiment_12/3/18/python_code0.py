import pulp

# Problem data
data = {
    'N': 6,
    'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]],
    'StartCity': 0
}

# Initialize model
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

# Sets and Parameters
N = data['N']
Distances = data['Distances']
StartCity = data['StartCity']

# Decision Variables
x = pulp.LpVariable.dicts('x', ((i, j) for i in range(N) for j in range(N)), cat='Binary')
u = pulp.LpVariable.dicts('u', (i for i in range(1, N)), 1, N-1, cat='Continuous')

# Objective Function
problem += pulp.lpSum(Distances[i][j] * x[i, j] for i in range(N) for j in range(N))

# Constraints
# Each town is visited exactly once
for i in range(N):
    problem += pulp.lpSum(x[i, j] for j in range(N) if i != j) == 1
    problem += pulp.lpSum(x[j, i] for j in range(N) if i != j) == 1

# Must start and return to StartCity
problem += pulp.lpSum(x[StartCity, j] for j in range(N) if StartCity != j) == 1
problem += pulp.lpSum(x[i, StartCity] for i in range(N) if StartCity != i) == 1

# Eliminate Subtours (MTZ)
for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + N * x[i, j] <= N - 1

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
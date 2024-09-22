import pulp

# Data from JSON
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

# Create a MILP problem
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N) if i != j), cat='Binary')

# Objective function
problem += pulp.lpSum(distances[i][j] * x[i, j] for i in range(N) for j in range(N) if i != j), "Total Distance"

# Constraints: each city is left exactly once
for i in range(N):
    if i != start_city:
        problem += pulp.lpSum(x[i, j] for j in range(N) if j != i) == 1, f"Leave_{i}"

# Constraints: each city is entered exactly once
for j in range(N):
    if j != start_city:
        problem += pulp.lpSum(x[i, j] for i in range(N) if i != j) == 1, f"Enter_{j}"

# Sub-tour elimination constraints
u = pulp.LpVariable.dicts("u", range(N), lowBound=1, upBound=N-1, cat='Integer')

for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + (N-1) * x[i, j] <= N-2, f"SubTourElimination_{i}_{j}"

# Solve the problem
problem.solve()

# Print the results
print(f'Status: {pulp.LpStatus[problem.status]}')

tour = []
for i in range(N):
    for j in range(N):
        if i != j and pulp.value(x[i, j]) == 1:
            tour.append((i, j))

print("Tour:", tour)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
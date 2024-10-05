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
Distances = data['Distances']
StartCity = data['StartCity']

# Initialize the problem
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')
u = pulp.LpVariable.dicts("u", range(1, N), lowBound=2, upBound=N, cat='Integer')

# Objective function
problem += pulp.lpSum(Distances[i][j] * x[i][j] for i in range(N) for j in range(N))

# Constraints
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N) if j != i) == 1, f"Leave_{i}"

for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N) if i != j) == 1, f"Enter_{j}"

for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1, f"Subtour_Elimination_{i}_{j}"

# Starting city constraints
problem += u[StartCity] == 1, "Start_Position"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
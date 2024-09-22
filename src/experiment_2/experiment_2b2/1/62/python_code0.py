import pulp

# Data from the input
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}

# Extract data
N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Initialize the problem
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Create decision variables
x = [[pulp.LpVariable(f'x_{i}_{j}', cat='Binary') for j in range(N)] for i in range(N)]
u = [pulp.LpVariable(f'u_{i}', lowBound=0, upBound=N-1, cat='Integer') for i in range(N)]

# Objective function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N))

# Constraints
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N) if j != i) == 1
    problem += pulp.lpSum(x[j][i] for j in range(N) if j != i) == 1

for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + (N - 1) * x[i][j] <= N - 2

# Solve the problem
problem.solve()

# Extracting the results
tour = []
current_city = start_city
for _ in range(N):
    tour.append(current_city)
    for j in range(N):
        if pulp.value(x[current_city][j]) == 1:
            current_city = j
            break

tour.append(start_city)
total_distance = pulp.value(problem.objective)

# Output format
output = {
    "visit_order": tour,
    "total_distance": total_distance
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
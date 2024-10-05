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
        [214, 267, 287, 484, 179, 0],
    ],
    'StartCity': 0
}

# Extracting the data from the JSON-like structure
N = data['N']
Distances = data['Distances']
start_city = data['StartCity']

# Initialize the LP problem
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts(
    "x",
    ((i, j) for i in range(N) for j in range(N)),
    cat=pulp.LpBinary
)

u = pulp.LpVariable.dicts("u", (i for i in range(N)), lowBound=0, upBound=N-1, cat=pulp.LpInteger)

# Objective function
problem += pulp.lpSum(Distances[i][j] * x[i, j] for i in range(N) for j in range(N))

# Constraints
for i in range(N):
    problem += pulp.lpSum(x[i, j] for j in range(N) if j != i) == 1

for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(N) if i != j) == 1

for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + N * x[i, j] <= N-1

# Solve the problem
problem.solve()

# Retrieve results
visit_order = []
current_city = start_city
visited = [False] * N

for step in range(N):
    visit_order.append(current_city)
    visited[current_city] = True
    for j in range(N):
        if x[current_city, j].varValue and not visited[j]:
            current_city = j
            break

visit_order.append(start_city)
total_distance = pulp.value(problem.objective)

# Output
output = {
    "visit_order": visit_order,
    "total_distance": total_distance
}

# Print the result
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp

# Initialize data
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

# Create the LP problem
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')
u = pulp.LpVariable.dicts("u", range(N), lowBound=0, upBound=N-1, cat='Continuous')

# Objective function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N))

# Constraints
for i in range(N):
    if i != start_city:
        problem += (pulp.lpSum(x[i][j] for j in range(N) if j != i) == 1)
    problem += (pulp.lpSum(x[j][i] for j in range(N) if j != i) == 1)

# Subtour elimination constraints
for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += (u[i] - u[j] + N * x[i][j] <= N-1)

# Ensure start and return to the start city
problem += (pulp.lpSum(x[start_city][j] for j in range(N) if j != start_city) == 1)
problem += (pulp.lpSum(x[i][start_city] for i in range(N) if i != start_city) == 1)

# Solve the problem
problem.solve()

# Extract solution
visit_order = [start_city]
current_city = start_city

for _ in range(N - 1):
    next_city = [j for j in range(N) if pulp.value(x[current_city][j]) == 1][0]
    visit_order.append(next_city)
    current_city = next_city

# Output results
total_distance_travelled = pulp.value(problem.objective)
print(f'Visit Order: {visit_order}')
print(f'Total Distance: {total_distance_travelled}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
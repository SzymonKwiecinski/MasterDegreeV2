import pulp

# Parse the data
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}
N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Problem setup
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N) if i != j), cat='Binary')

# Objective function
problem += pulp.lpSum(distances[i][j] * x[(i, j)] for i in range(N) for j in range(N) if i != j)

# Constraints
for i in range(N):
    problem += pulp.lpSum(x[(i, j)] for j in range(N) if i != j) == 1
    problem += pulp.lpSum(x[(j, i)] for j in range(N) if i != j) == 1

# Subtour elimination constraints
u = pulp.LpVariable.dicts("u", range(N), lowBound=0, upBound=N-1, cat='Continuous')

for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + N * x[(i, j)] <= N - 1

# Start city constraints
for j in range(N):
    if j != start_city:
        problem += x[(start_city, j)] == 1
        problem += x[(j, start_city)] == 1

# Solve the problem
problem.solve()

# Extracting the visit order and total distance
visit_order = []
current_city = start_city
while len(visit_order) < N:
    visit_order.append(current_city)
    next_city = [j for j in range(N) if current_city != j and pulp.value(x[(current_city, j)]) == 1][0]
    current_city = next_city

total_distance = pulp.value(problem.objective)

# Output the results
print(f'Visit Order: {visit_order}')
print(f'Total Distance: {total_distance} (Objective Value): <OBJ>{total_distance}</OBJ>')
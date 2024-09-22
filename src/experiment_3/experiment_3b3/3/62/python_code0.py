import pulp

# Parse the data
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}
N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Create the problem
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts('x', ((i, j) for i in range(N) for j in range(N)), cat='Binary')
u = pulp.LpVariable.dicts('u', (i for i in range(N)), lowBound=0, upBound=N-1, cat='Continuous')

# Objective function
problem += pulp.lpSum(distances[i][j] * x[i, j] for i in range(N) for j in range(N))

# Constraints
# Each city must be visited exactly once
for i in range(N):
    problem += pulp.lpSum(x[i, j] for j in range(N) if j != i) == 1

# Each city must be departed from exactly once
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(N) if i != j) == 1

# Subtour elimination constraints
for i in range(N):
    for j in range(N):
        if i != j:
            problem += u[i] - u[j] + N * x[i, j] <= N - 1

# The traveler must start and end at the designated start city
problem += pulp.lpSum(x[start_city, j] for j in range(N) if j != start_city) == 1
problem += pulp.lpSum(x[j, start_city] for j in range(N) if j != start_city) == 1

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
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

# Problem
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat='Binary')

# Objective Function
problem += pulp.lpSum(Distances[i][j] * x[i, j] for i in range(N) for j in range(N))

# Constraints
for i in range(N):
    problem += pulp.lpSum(x[i, j] for j in range(N) if i != j) == 1

for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(N) if i != j) == 1

# Subtour Elimination Constraints (Miller-Tucker-Zemlin)
u = pulp.LpVariable.dicts("u", range(N), 0, N-1, cat='Integer')

for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + N*x[i, j] <= N-1

# Solve the problem
problem.solve()

# Output the results
visit_order = []
current_city = data['StartCity']
visit_order.append(current_city)

for _ in range(N - 1):
    next_city = None
    for j in range(N):
        if pulp.value(x[current_city, j]) == 1:
            next_city = j
            break
    if next_city is not None:
        visit_order.append(next_city)
        current_city = next_city

total_distance = pulp.value(problem.objective)

print(f"Visit Order: {visit_order}")
print(f"Total Distance: {total_distance}")
print(f" (Objective Value): <OBJ>{total_distance}</OBJ>")
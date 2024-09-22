import pulp
import json

# Data input
data = json.loads("{'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}")

N = data['N']
distances = data['Distances']
start_city = data['StartCity']
C = list(range(N))

# Problem definition
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", [(i, j) for i in C for j in C], cat='Binary')
u = pulp.LpVariable.dicts("u", range(N), lowBound=1)

# Objective function
problem += pulp.lpSum(distances[i][j] * x[i, j] for i in C for j in C), "Total_Distance"

# Constraints
# Out-degree constraint for the start city
problem += pulp.lpSum(x[start_city, j] for j in C if j != start_city) == 1

# In-degree constraint for each city except the start city
for j in C:
    if j != start_city:
        problem += pulp.lpSum(x[i, j] for i in C) == 1

# Subtour elimination constraints
for i in C:
    for j in C:
        if i != j and i != start_city and j != start_city:
            problem += u[i] - u[j] + N * x[i, j] <= N - 1

# Position variable constraint
for i in C:
    if i != start_city:
        problem += u[i] >= 1

# Solve the problem
problem.solve()

# Extract the results
visit_order = []
for i in C:
    for j in C:
        if pulp.value(x[i, j]) == 1:
            visit_order.append(j)
total_distance = pulp.value(problem.objective)

# Output the results
print(f'Visit order: {visit_order}')
print(f'Total distance: {total_distance}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
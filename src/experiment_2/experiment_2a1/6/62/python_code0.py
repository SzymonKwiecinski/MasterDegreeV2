import pulp
import json

# Data provided in JSON format
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267],
                              [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484],
                              [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]],
        'StartCity': 0}

distances = data['Distances']
start_city = data['StartCity']
N = data['N']

# Create the problem
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision variables
routes = pulp.LpVariable.dicts("Route", (range(N), range(N)), cat='Binary')

# Objective function
problem += pulp.lpSum(distances[i][j] * routes[i][j] for i in range(N) for j in range(N) if i != j)

# Constraints
problem += pulp.lpSum(routes[start_city][j] for j in range(N) if j != start_city) == 1  # Start city to one other city
for j in range(N):
    if j != start_city:
        problem += pulp.lpSum(routes[i][j] for i in range(N) if i != j) == 1  # Each city must be entered exactly once
        problem += pulp.lpSum(routes[j][i] for i in range(N) if i != j) == 1  # Each city must be left exactly once

# Subtour elimination constraints
u = pulp.LpVariable.dicts('u', range(N), lowBound=0, upBound=N-1, cat='Integer')
for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + (N - 1) * routes[i][j] <= N - 2

# Solve the problem
problem.solve()

# Retrieve the tour
visit_order = []
current_city = start_city

while True:
    for j in range(N):
        if pulp.value(routes[current_city][j]) == 1:
            visit_order.append(j)
            current_city = j
            break
    if current_city == start_city and len(visit_order) == N:
        break

total_distance = pulp.value(problem.objective)

# Prepare the output
output = {
    "visit_order": [start_city] + visit_order + [start_city],
    "total_distance": total_distance
}

# Print the output
print(output)
print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
import pulp
import numpy as np
import json

data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}

N = data['N']
distances = np.array(data['Distances'])
start_city = data['StartCity']

# Create the linear program
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')

# Objective function: Minimize the total distance
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N) if i != j)

# Constraints
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N) if i != j) == 1  # Each city j is entered once

for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N) if j != i) == 1  # Each city i is exited once

# Subtour elimination constraints
subtour_constraints = []
for s in range(2, N):
    for subset in combinations(range(N), s):
        problem += pulp.lpSum(x[i][j] for i in subset for j in subset if i != j) <= len(subset) - 1

# Start city constraints
for j in range(N):
    if j != start_city:
        problem += x[start_city][j] == 1  # Start from the starting city
        problem += x[j][start_city] == 0  # Don't return to the start city immediately

# Solve the problem
problem.solve()

# Retrieve the visit order
visit_order = [start_city]
current_city = start_city

while len(visit_order) < N:
    for j in range(N):
        if x[current_city][j].varValue == 1:
            visit_order.append(j)
            current_city = j
            break

# Return to the start city
visit_order.append(start_city)

# Calculate total distance
total_distance = pulp.value(problem.objective)

# Output preparation
output = {
    "visit_order": visit_order,
    "total_distance": total_distance
}

print(output)
print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
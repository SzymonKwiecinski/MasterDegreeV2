import pulp
import numpy as np
import json

# Given data in JSON format
data = {'N': 6, 
        'Distances': [[0, 182, 70, 399, 56, 214], 
                      [182, 0, 255, 229, 132, 267], 
                      [70, 255, 0, 472, 127, 287], 
                      [399, 229, 472, 0, 356, 484], 
                      [56, 132, 127, 356, 0, 179], 
                      [214, 267, 287, 484, 179, 0]], 
        'StartCity': 0}

# Extracting values from data
N = data['N']
distances = np.array(data['Distances'])
start_city = data['StartCity']

# Define the problem
problem = pulp.LpProblem("TravelingSalesman", pulp.LpMinimize)

# Create decision variables
x = pulp.LpVariable.dicts('x', (range(N), range(N)), cat='Binary')

# Objective Function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N) if i != j)

# Constraints
# Each city must be left once
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N) if i != j) == 1

# Each city must be entered once
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N) if i != j) == 1

# Subtour elimination constraints
u = pulp.LpVariable.dicts('u', range(N), lowBound=0, upBound=N-1, cat='Integer')

for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + (N - 1) * x[i][j] <= N - 2

# Set the starting city
for j in range(1, N):
    problem += x[start_city][j] == 1

# Solve the problem
problem.solve()

# Extract the results
visit_order = [start_city]
current_city = start_city

while True:
    for j in range(N):
        if pulp.value(x[current_city][j]) == 1:
            visit_order.append(j)
            current_city = j
            break
    if current_city == start_city or len(visit_order) == N + 1:
        break

# Calculate total distance
total_distance = pulp.value(problem.objective)

# Output format
result = {
    "visit_order": visit_order,
    "total_distance": total_distance
}

print(result)
print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
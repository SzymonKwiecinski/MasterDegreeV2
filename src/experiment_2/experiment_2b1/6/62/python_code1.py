import pulp
import json

# Input data
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], 
                               [182, 0, 255, 229, 132, 267], 
                               [70, 255, 0, 472, 127, 287], 
                               [399, 229, 472, 0, 356, 484], 
                               [56, 132, 127, 356, 0, 179], 
                               [214, 267, 287, 484, 179, 0]], 
        'StartCity': 0}

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Create the model
problem = pulp.LpProblem("TravelingSalesmanProblem", pulp.LpMinimize)

# Create decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')

# Objective function: minimize the total distance traveled
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N) if i != j)

# Constraints
for j in range(N):
    if j != start_city:
        problem += pulp.lpSum(x[i][j] for i in range(N) if i != j) == 1  # Each town is visited exactly once
        problem += pulp.lpSum(x[j][i] for i in range(N) if i != j) == 1  # Each town is left exactly once

# Subtour elimination constraints
u = pulp.LpVariable.dicts("u", range(N), lowBound=0, upBound=N-1, cat='Integer')
for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + (N-1) * x[i][j] <= N-2

# The start city constraints
for j in range(N):
    if j != start_city:
        problem += pulp.lpSum(x[start_city][j] for j in range(N)) == 1

# Solve the problem
problem.solve()

# Extracting the visit order
visit_order = [start_city]
current_city = start_city

# Track the visited cities
visited = set(visit_order)

while len(visited) < N:
    for j in range(N):
        if x[current_city][j].varValue == 1 and j not in visited: 
            visit_order.append(j)
            visited.add(j)
            current_city = j
            break

# Return to start city
visit_order.append(start_city)

# Calculate total distance
total_distance = pulp.value(problem.objective)

# Output result
result = {
    "visit_order": visit_order,
    "total_distance": total_distance
}

print(result)
print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
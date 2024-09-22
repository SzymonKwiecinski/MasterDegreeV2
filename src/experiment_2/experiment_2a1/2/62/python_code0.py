import pulp
import numpy as np

data = {
    'N': 6,
    'Distances': [[0, 182, 70, 399, 56, 214], 
                  [182, 0, 255, 229, 132, 267], 
                  [70, 255, 0, 472, 127, 287], 
                  [399, 229, 472, 0, 356, 484], 
                  [56, 132, 127, 356, 0, 179], 
                  [214, 267, 287, 484, 179, 0]], 
    'StartCity': 0
}

N = data['N']
distances = np.array(data['Distances'])
start_city = data['StartCity']

# Create the problem
problem = pulp.LpProblem("TravelingSalesmanProblem", pulp.LpMinimize)

# Create decision variables
routes = pulp.LpVariable.dicts("Route", (range(N), range(N)), cat='Binary')

# Objective function
problem += pulp.lpSum(distances[i][j] * routes[i][j] for i in range(N) for j in range(N) if i != j)

# Constraints
# Each city must be entered and left exactly once
for k in range(N):
    problem += pulp.lpSum(routes[i][k] for i in range(N) if i != k) == 1
    problem += pulp.lpSum(routes[k][j] for j in range(N) if j != k) == 1

# Subtour elimination constraints
u = pulp.LpVariable.dicts("u", range(N), lowBound=0, cat='Integer')
problem += u[start_city] == 1  # Start from the starting city

for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + (N - 1) * routes[i][j] <= N - 2

# Solve the problem
problem.solve()

# Extract the visit order
visit_order = []
current_city = start_city
visit_order.append(current_city)

while len(visit_order) < N + 1:
    for j in range(N):
        if current_city != j and pulp.value(routes[current_city][j]) == 1:
            visit_order.append(j)
            current_city = j
            break

# Add the starting city to the end to complete the tour
visit_order.append(start_city)

# Calculate total distance
total_distance = pulp.value(problem.objective)

# Output result
result = {
    "visit_order": visit_order,
    "total_distance": total_distance
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
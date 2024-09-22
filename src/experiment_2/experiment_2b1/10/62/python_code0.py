import pulp
import json

# Data input
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Create the problem
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Variables: x[i][j] is 1 if traveling from city i to city j
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')

# Objective function: minimize total traveling distance
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N) if i != j)

# Constraints
# Each city must be entered and exited exactly once
for k in range(N):
    problem += pulp.lpSum(x[k][j] for j in range(N) if j != k) == 1
    problem += pulp.lpSum(x[i][k] for i in range(N) if i != k) == 1

# Subtour elimination constraints
u = pulp.LpVariable.dicts("u", range(N), lowBound=0, cat='Integer')
for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + (N - 1) * x[i][j] <= N - 2

# Traveling back to the start city
problem += x[start_city][start_city] == 0

# Solve the problem
problem.solve()

# Extracting the route
visit_order = []
current_city = start_city
for _ in range(N):
    for j in range(N):
        if x[current_city][j].value() == 1:
            visit_order.append(j)
            current_city = j
            break
visit_order.insert(0, start_city)
visit_order.append(start_city)

total_distance = pulp.value(problem.objective)

# Output the results
output = {
    "visit_order": visit_order,
    "total_distance": total_distance
}

print(output)
print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
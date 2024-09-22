import pulp
import json

# Input data in JSON format
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Create a linear programming problem
problem = pulp.LpProblem("TravelingSalesmanProblem", pulp.LpMinimize)

# Create decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')

# Objective function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N) if i != j)

# Constraints
for k in range(N):
    if k != start_city:
        problem += pulp.lpSum(x[start_city][j] for j in range(N) if j != start_city) == 1
        problem += pulp.lpSum(x[j][start_city] for j in range(N) if j != start_city) == 1

# Each city must be visited exactly once
for j in range(N):
    if j != start_city:
        problem += pulp.lpSum(x[i][j] for i in range(N) if i != j) == 1
        problem += pulp.lpSum(x[j][i] for i in range(N) if i != j) == 1

# Eliminate sub-tours using Miller-Tucker-Zemlin constraints
u = pulp.LpVariable.dicts("u", range(N), lowBound=0, upBound=N-1)

for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + (N-1) * x[i][j] <= N-2

# Solve the problem
problem.solve()

# Extract the route and total distance
visit_order = [start_city]
total_distance = 0

# Find the route based on the decision variables
current_city = start_city
while len(visit_order) < N + 1:
    for j in range(N):
        if x[current_city][j].varValue == 1:
            visit_order.append(j)
            total_distance += distances[current_city][j]
            current_city = j
            break

# Return to start city
total_distance += distances[current_city][start_city]
visit_order.append(start_city)

# Output result
result = {
    "visit_order": visit_order,
    "total_distance": total_distance
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
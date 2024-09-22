import pulp
import json

data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Create the optimization problem
problem = pulp.LpProblem("TravelingSalesmanProblem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')

# Objective function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N) if i != j)

# Constraints
for k in range(N):
    if k != start_city:
        problem += pulp.lpSum(x[start_city][k] for k in range(N) if k != start_city) == 1
    problem += pulp.lpSum(x[k][start_city] for k in range(N) if k != start_city) == 1

for i in range(N):
    for j in range(N):
        if i != j:
            problem += x[i][j] + x[j][i] <= 1

# Solve the problem
problem.solve()

# Extract visit order
visit_order = [start_city]
current_city = start_city

while len(visit_order) < N + 1:
    for j in range(N):
        if x[current_city][j].varValue == 1:
            visit_order.append(j)
            current_city = j
            break

visit_order.append(start_city)

# Calculate total distance
total_distance = pulp.value(problem.objective)

# Prepare output
output = {
    "visit_order": visit_order,
    "total_distance": total_distance
}

print(output)
print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
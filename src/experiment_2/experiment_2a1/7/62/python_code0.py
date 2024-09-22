import pulp
import json

# Input data
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Create problem variable
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts('x', (range(N), range(N)), cat='Binary')

# Objective function: minimize the total distance traveled
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N) if i != j)

# Constraints
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N) if i != j) == 1  # Each city must be left once
    problem += pulp.lpSum(x[j][i] for i in range(N) if i != j) == 1  # Each city must be entered once

# Subtour elimination constraints
u = pulp.LpVariable.dicts('u', range(N), lowBound=0, upBound=N-1, cat='Integer')
for i in range(1, N):  # Skip the first city
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + (N-1) * x[i][j] <= N - 2

# Ensure the traveler starts and ends at the start_city
for j in range(N):
    if j != start_city:
        problem += x[start_city][j] == x[j][start_city] == 0

problem.solve()

# Extracting the visit order and total distance
visit_order = [start_city]
current_city = start_city
while len(visit_order) < N + 1:
    for j in range(N):
        if x[current_city][j].varValue == 1:
            visit_order.append(j)
            current_city = j
            break
visit_order.append(start_city)

total_distance = pulp.value(problem.objective)

# Output
output = {
    "visit_order": visit_order,
    "total_distance": total_distance
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp
import json

# Input data
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Create the problem
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts('x', (range(N), range(N)), 0, 1, pulp.LpBinary)
u = pulp.LpVariable.dicts('u', range(N), 0, N, pulp.LpInteger)

# Objective function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N) if i != j)

# Constraints
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N) if i != j) == 1  # Each city must be entered exactly once

for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N) if j != i) == 1  # Each city must be left exactly once

problem += u[start_city] == 0  # Start from the start_city

for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + (N-1) * x[i][j] <= N - 2  # Subtour elimination

# Solve the problem
problem.solve()

# Get the visit order
visit_order = []
current_city = start_city
for _ in range(N):
    for next_city in range(N):
        if x[current_city][next_city].value() == 1:
            visit_order.append(next_city)
            current_city = next_city
            break
visit_order.insert(0, start_city)  # Add starting city at the beginning
visit_order.append(start_city)  # Return to starting city

# Calculate total distance
total_distance = pulp.value(problem.objective)

# Prepare the output
output = {
    "visit_order": visit_order,
    "total_distance": total_distance
}

print(output)
print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
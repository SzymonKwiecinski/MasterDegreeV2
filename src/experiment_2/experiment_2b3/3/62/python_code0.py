import pulp
import numpy as np

# Read data
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}
N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Initialize the problem
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", [(i, j) for i in range(N) for j in range(N)], cat=pulp.LpBinary)
u = pulp.LpVariable.dicts("u", range(N), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(distances[i][j] * x[i, j] for i in range(N) for j in range(N))

# Constraints
# Ensure each city is entered and exited exactly once
for i in range(N):
    problem += pulp.lpSum(x[i, j] for j in range(N) if j != i) == 1
    problem += pulp.lpSum(x[j, i] for j in range(N) if j != i) == 1

# Subtour elimination (Miller-Tucker-Zemlin formulation)
for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + N * x[i, j] <= N - 1

# Solve the problem
problem.solve()

# Determine the visit order
visit_order = [start_city]
current_city = start_city
while len(visit_order) < N + 1:
    for j in range(N):
        if pulp.value(x[current_city, j]) == 1:
            visit_order.append(j)
            current_city = j
            break

# Calculate total distance
total_distance = pulp.value(problem.objective)

# Output
output = {
    "visit_order": visit_order,
    "total_distance": total_distance
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
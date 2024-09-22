import pulp
import json

# Data from the given JSON format
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Initialize the problem
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts('x', (range(N), range(N)), cat='Binary')
u = pulp.LpVariable.dicts('u', range(N), lowBound=1, upBound=N-1, cat='Integer')

# Objective function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N)), "Total Distance"

# Constraints
# Each city must be entered and exited exactly once
for j in range(N):
    problem += pulp.lpSum(x[start_city][j] for j in range(N)) == 1, f"Enter_Constraint_{j}"
for i in range(N):
    problem += pulp.lpSum(x[i][start_city] for i in range(N)) == 1, f"Exit_Constraint_{i}"

# Flow conservation constraint
for i in range(N):
    problem += (pulp.lpSum(x[i][j] for j in range(N)) - pulp.lpSum(x[j][i] for j in range(N))) == 0, f"Flow_Conservation_{i}"

# Subtour elimination constraints (Miller-Tucker-Zemlin)
for i in range(N):
    for j in range(N):
        if i != j:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1, f"Subtour_Constraint_{i}_{j}"

# Solve the problem
problem.solve()

# Retrieve the optimal route
visit_order = []
total_distance = pulp.value(problem.objective)

for i in range(N):
    for j in range(N):
        if pulp.value(x[i][j]) == 1:
            visit_order.append((i, j))

# Print the total distance and visit order
print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
print("Visit Order:", visit_order)
import pulp
import json

# Data input
data = json.loads('{"N": 6, "Distances": [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], "StartCity": 0}')

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Problem definition
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), 0, 1, pulp.LpBinary)
u = pulp.LpVariable.dicts("u", range(N), lowBound=1, cat='Continuous')

# Objective function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N)), "Total_Distance"

# Constraints
# Each town must be visited exactly once
problem += pulp.lpSum(x[start_city][j] for j in range(N)) == 1, "Start_Constraint"

for j in range(N):
    if j != start_city:
        problem += pulp.lpSum(x[i][j] for i in range(N)) == 1, f"Visit_Constraint_{j}"

problem += pulp.lpSum(x[j][start_city] for j in range(N) if j != start_city) == 1, "Return_Constraint"

# Subtour elimination constraints
for i in range(N):
    for j in range(N):
        if i != j and i != start_city and j != start_city:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1, f"Subtour_Constraint_{i}_{j}"

# Solve the problem
problem.solve()

# Output results
visit_order = []
total_distance = pulp.value(problem.objective)

for i in range(N):
    for j in range(N):
        if pulp.value(x[i][j]) == 1:
            visit_order.append((i, j))

# Get the actual visit order
visit_sequence = [start_city]
current_city = start_city
for _ in range(N - 1):  # Fixed to not use while loop
    for j in range(N):
        if pulp.value(x[current_city][j]) == 1:
            visit_sequence.append(j)
            current_city = j
            break

# Print the objective value
print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
print(f'Visit Order: {visit_sequence}')
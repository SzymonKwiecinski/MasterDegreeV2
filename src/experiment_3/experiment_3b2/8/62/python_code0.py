import pulp
import json

# Input data in JSON format
data = json.loads('{"N": 6, "Distances": [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], "StartCity": 0}')

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Problem definition
problem = pulp.LpProblem("TSP_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N + 1) for j in range(N + 1)), cat='Binary')
u = pulp.LpVariable.dicts("u", (i for i in range(1, N + 1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(distances[i][j] * x[i, j] for i in range(N + 1) for j in range(N + 1)), "Total_Distance"

# Constraints
# Ensure each city is departed from exactly once
for i in range(N + 1):
    problem += pulp.lpSum(x[i, j] for j in range(N + 1) if j != i) == 1, f"Departure_Constraint_{i}"

# Ensure each city is arrived at exactly once
for j in range(N + 1):
    problem += pulp.lpSum(x[i, j] for i in range(N + 1) if i != j) == 1, f"Arrival_Constraint_{j}"

# Subtour elimination constraints
for i in range(1, N + 1):
    for j in range(1, N + 1):
        if i != j:
            problem += u[i] - u[j] + N * x[i, j] <= N - 1, f"Subtour_Constraint_{i}_{j}"

# Reference point for subtour elimination
problem += u[0] == 0, "Subtour_Reference"

# Solve the problem
problem.solve()

# Output the results
visit_order = []
total_distance = pulp.value(problem.objective)

for i in range(N + 1):
    for j in range(N + 1):
        if pulp.value(x[i, j]) == 1:
            if i == start_city:
                visit_order.append(j)

print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
print(f'Visit Order: {visit_order}')
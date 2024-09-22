import pulp
import json

# Data in JSON format
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267],
                              [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484],
                              [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 
        'StartCity': 0}

# Extract values from data
N = data['N']
Distances = data['Distances']
start_city = data['StartCity']

# Create the problem instance
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

# Define sets
C = list(range(N + 1))

# Define variables
x = pulp.LpVariable.dicts("x", (C, C), 0, 1, pulp.LpBinary)
u = pulp.LpVariable.dicts("u", C[1:], 0, N-1)

# Objective function
problem += pulp.lpSum(Distances[i][j] * x[i][j] for i in C for j in C), "Total_Distance"

# Constraints
# Each city must be entered and exited exactly once (except the starting city)
for i in C[1:]:
    problem += pulp.lpSum(x[i][j] for j in C) == 1, f"Exit_City_{i}"
    problem += pulp.lpSum(x[j][i] for j in C) == 1, f"Enter_City_{i}"

# Subtour elimination constraints
for i in C[1:]:
    for j in C[1:]:
        if i != j:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1, f"Subtour_Elimination_{i}_{j}"

# Solve the problem
problem.solve()

# Extract the visit order
visit_order = []
for i in C:
    for j in C:
        if pulp.value(x[i][j]) == 1 and i == start_city:
            visit_order.append(j)

# Calculate total distance
total_distance = pulp.value(problem.objective)

# Output results
print(f'Visit Order: {visit_order}')
print(f'Total Distance: {total_distance}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
from pulp import LpProblem, LpVariable, lpSum, LpBinary, LpMinimize, value
import numpy as np

# Parsing the data from JSON format
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Create the problem
problem = LpProblem("TSP", LpMinimize)

# Variables
x = LpVariable.dicts("x", [(i, j) for i in range(N) for j in range(N) if i != j], cat=LpBinary)

# Objective
problem += lpSum(distances[i][j] * x[i, j] for i in range(N) for j in range(N) if i != j)

# Constraints
for i in range(N):
    # Each city can be departed from exactly once, except for returning to the start city
    problem += lpSum(x[i, j] for j in range(N) if j != i) == 1

    # Each city must be entered exactly once
    problem += lpSum(x[j, i] for j in range(N) if j != i) == 1

# Subtour elimination constraints
u = LpVariable.dicts("u", range(N), 0, N-1, LpBinary)
for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + (N - 1) * x[i, j] <= N - 2

# Solve the problem
problem.solve()

# Retrieve the solution
visit_sequence = [start_city]
current_city = start_city

for _ in range(N - 1):
    for j in range(N):
        if current_city != j and x[current_city, j].varValue == 1:
            visit_sequence.append(j)
            current_city = j
            break
visit_sequence.append(start_city)

total_distance = value(problem.objective)

# Output the result
output = {
    "visit_order": visit_sequence,
    "total_distance": total_distance
}

print(output)
print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
from pulp import LpProblem, LpVariable, lpSum, LpBinary, LpMinimize, LpStatus, value
import numpy as np

# Parsing the data from JSON format
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Create the problem
problem = LpProblem("TSP", LpMinimize)

# Variables
x = LpVariable.dicts("x", [(i, j) for i in range(N) for j in range(N)], cat=LpBinary)
u = LpVariable.dicts("u", [i for i in range(N)], lowBound=0, cat='Continuous')

# Objective
problem += lpSum(distances[i][j] * x[i, j] for i in range(N) for j in range(N))

# Constraints
# Start city constraints
for j in range(1, N):
    problem += x[start_city, j] == 1

# Return to start city
for i in range(1, N):
    problem += x[i, start_city] == 1

# Visit each city once, except the start city
for i in range(1, N):
    problem += lpSum(x[i, j] for j in range(N) if j != i) == 1

for j in range(1, N):
    problem += lpSum(x[i, j] for i in range(N) if i != j) == 1

# Subtour elimination constraints
for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + N * x[i, j] <= N - 1

# Solve the problem
problem.solve()

# Retrieve the solution
visit_sequence = [start_city]
current_city = start_city

while len(visit_sequence) < N:
    for j in range(N):
        if x[current_city, j].varValue == 1 and j not in visit_sequence:
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
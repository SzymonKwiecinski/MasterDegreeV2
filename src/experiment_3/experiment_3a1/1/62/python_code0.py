import pulp
import json

# Input data
data_json = '{"N": 6, "Distances": [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], "StartCity": 0}'
data = json.loads(data_json)

# Parameters
N = data['N']
distances = data['Distances']
start_city = data['StartCity']
C = range(N + 1)  # Including start city

# Problem definition
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts('x', (C, C), 0, 1, pulp.LpBinary)
u = pulp.LpVariable.dicts('u', C, lowBound=0, upBound=N)

# Objective Function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in C for j in C)

# Constraints
# Each city is visited exactly once
for s in C:
    if s == start_city:
        problem += pulp.lpSum(x[start_city][j] for j in C) == 1
    else:
        problem += pulp.lpSum(x[i][s] for i in C) == 1
        problem += pulp.lpSum(x[s][j] for j in C) == 1

# Subtour elimination constraints
for i in C:
    for j in C:
        if i != j and i != start_city and j != start_city:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1

# Solve the problem
problem.solve()

# Output results
visit_order = []
for i in C:
    for j in C:
        if pulp.value(x[i][j]) == 1:
            visit_order.append(j)

total_distance = pulp.value(problem.objective)

print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
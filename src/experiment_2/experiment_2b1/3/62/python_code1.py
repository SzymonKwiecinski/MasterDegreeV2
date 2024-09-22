import json
import pulp

# Input data
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], 
                               [182, 0, 255, 229, 132, 267], 
                               [70, 255, 0, 472, 127, 287], 
                               [399, 229, 472, 0, 356, 484], 
                               [56, 132, 127, 356, 0, 179], 
                               [214, 267, 287, 484, 179, 0]], 
        'StartCity': 0}

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Create the problem
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Create variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')
u = pulp.LpVariable.dicts("u", range(N), lowBound=0, upBound=N, cat='Integer')

# Objective function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N) if i != j)

# Constraints
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N) if i != j) == 1  # Each city i is visited exactly once
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N) if i != j) == 1  # Each city j is left exactly once

# Subtour elimination (Miller-Tucker-Zemlin)
for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + (N - 1) * x[i][j] <= N - 2

# Solve the problem
problem.solve()

# Extracting the visit order
visit_order = [start_city]
current_city = start_city
while len(visit_order) < N + 1:
    for j in range(N):
        if x[current_city][j].varValue == 1:
            visit_order.append(j)
            current_city = j
            break
visit_order.append(start_city)  # Return to start_city

# Total distance
total_distance = pulp.value(problem.objective)

# Output result
result = {
    "visit_order": visit_order,
    "total_distance": total_distance
}
print(result)
print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
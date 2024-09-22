import pulp
import json

# Load data
data = json.loads('{"N": 6, "Distances": [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], "StartCity": 0}')

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Define the problem
problem = pulp.LpProblem('TSP', pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts('x', (range(N+1), range(N+1)), cat='Binary')
u = pulp.LpVariable.dicts('u', range(1, N+1), lowBound=1, cat='Continuous')

# Objective function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N+1) for j in range(N+1))

# Constraints
# Each town must be visited exactly once
problem += pulp.lpSum(x[start_city][j] for j in range(1, N+1)) == 1  # Start from start_city
for i in range(1, N+1):
    problem += pulp.lpSum(x[i][j] for j in range(N+1)) == 1  # Each town visited once

# Return to the start city
problem += pulp.lpSum(x[j][start_city] for j in range(1, N+1)) == 1

# Subtour elimination constraints
for i in range(1, N+1):
    for j in range(1, N+1):
        if i != j:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1

# Solve the problem
problem.solve()

# Retrieve the visit order and total distance
visit_order = []
for i in range(N+1):
    for j in range(N+1):
        if pulp.value(x[i][j]) == 1:
            visit_order.append(j)

total_distance = pulp.value(problem.objective)

# Output the results
print(f'Visit Order: {visit_order}')
print(f'Total Distance: {total_distance}')
print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
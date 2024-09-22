import pulp
import json

# Given data
data = {
    'N': 6,
    'Distances': [[0, 182, 70, 399, 56, 214], 
                  [182, 0, 255, 229, 132, 267], 
                  [70, 255, 0, 472, 127, 287], 
                  [399, 229, 472, 0, 356, 484], 
                  [56, 132, 127, 356, 0, 179], 
                  [214, 267, 287, 484, 179, 0]], 
    'StartCity': 0
}

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Define the problem
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts('x', (range(N), range(N)), cat='Binary')
u = pulp.LpVariable.dicts('u', range(1, N), lowBound=1, upBound=N-1)

# Objective function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N) if i != j), "Total_Distance"

# Constraints: Each city must be visited exactly once
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N) if j != i) == 1
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N) if i != j) == 1

# Subtour elimination constraints
for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1

# Solve the problem
problem.solve()

# Prepare the output
visit_order = []
total_distance = pulp.value(problem.objective)

for i in range(N):
    for j in range(N):
        if pulp.value(x[i][j]) == 1:
            visit_order.append((i, j))  # Store the route in order

# Extract the visit order
final_order = [start_city]
for i in range(len(visit_order)):
    if visit_order[i][0] == final_order[-1]:
        final_order.append(visit_order[i][1])
final_order.append(start_city)

print(f'Visit Order: {final_order}')
print(f'Total Distance: {total_distance}')
print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
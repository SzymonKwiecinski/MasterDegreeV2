import pulp
import json

# Given data
data_json = '''{'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}'''
data = json.loads(data_json)

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Create the problem
problem = pulp.LpProblem("TSP_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')

# Objective function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N))

# Constraints
for j in range(N):
    problem += pulp.lpSum(x[start_city][j] for j in range(N)) == 1  # Leaving the start city

for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N) if i != j) == 1  # Each town must be left exactly once

for i in range(N):
    problem += pulp.lpSum(x[j][i] for j in range(N) if j != i) == 1  # Each town must be entered exactly once

# Subtour elimination constraints
u = pulp.LpVariable.dicts("u", range(N), lowBound=0, upBound=N-1, cat='Continuous')

for i in range(N):
    for j in range(N):
        if i != j:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1

# Solve the problem
problem.solve()

# Output the visit order and total distance
visit_order = []
for i in range(N):
    for j in range(N):
        if pulp.value(x[i][j]) == 1:
            visit_order.append(j)

total_distance = pulp.value(problem.objective)

print(f'Visit Order: {visit_order}')
print(f'Total Distance: {total_distance}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
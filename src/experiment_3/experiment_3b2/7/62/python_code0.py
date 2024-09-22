import pulp
import json

# Data provided in JSON format
data = json.loads('{"N": 6, "Distances": [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], "StartCity": 0}')

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Create the problem variable
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')
u = pulp.LpVariable.dicts("u", range(N), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N) if i != j)

# Constraints
# Leave each city exactly once
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N) if j != i) == 1

# Enter each city exactly once
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N) if i != j) == 1

# Starting city constraint
problem += u[start_city] == 0

# Subtour elimination constraints
for i in range(N):
    for j in range(N):
        if i != j and i != start_city and j != start_city:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1

# Solve the problem
problem.solve()

# Collecting the results
visit_order = []
total_distance = pulp.value(problem.objective)

# Finding the visit order
current_city = start_city
while len(visit_order) < N:
    visit_order.append(current_city)
    for j in range(N):
        if j != current_city and pulp.value(x[current_city][j]) == 1:
            current_city = j
            break

print(f'Visit Order: {visit_order}')
print(f'Total Distance: {total_distance}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
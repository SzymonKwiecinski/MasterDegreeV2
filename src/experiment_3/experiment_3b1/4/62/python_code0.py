import pulp
import json

# Data input
data = json.loads('{"N": 6, "Distances": [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], "StartCity": 0}')
N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Defining the problem
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision variables
cities = range(N)
x = pulp.LpVariable.dicts("x", ((i, j) for i in cities for j in cities), cat='Binary')
u = pulp.LpVariable.dicts("u", cities, lowBound=1, cat='Continuous')

# Objective function
problem += pulp.lpSum(distances[i][j] * x[i, j] for i in cities for j in cities)

# Constraints
# Each city must be visited exactly once
problem += pulp.lpSum(x[start_city, j] for j in cities) == 1
problem += pulp.lpSum(x[j, start_city] for j in cities) == 1

for i in cities:
    if i != start_city:
        problem += pulp.lpSum(x[i, j] for j in cities) == 1
        problem += pulp.lpSum(x[j, i] for j in cities) == 1

# Subtour elimination constraints
for i in cities:
    for j in cities:
        if i != j and i != start_city and j != start_city:
            problem += u[i] - u[j] + N * x[i, j] <= N - 1

# Solve the problem
problem.solve()

# Extracting results
visit_order = [start_city]
for i in cities:
    for j in cities:
        if pulp.value(x[i, j]) == 1:
            visit_order.append(j)

total_distance = pulp.value(problem.objective)

# Output results
print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
print('Visit Order:', visit_order)
import pulp
import json

# Data as given
data = {'N': 6, 
        'Distances': [[0, 182, 70, 399, 56, 214], 
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

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')
u = pulp.LpVariable.dicts("u", range(N), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N))

# Constraints
for j in range(N):
    if j != start_city:
        problem += pulp.lpSum(x[start_city][j] for j in range(N)) == 1
        problem += pulp.lpSum(x[j][start_city] for j in range(N)) == 1

for j in range(N):
    if j != start_city:
        problem += pulp.lpSum(x[i][j] for i in range(N)) == 1
        problem += pulp.lpSum(x[j][i] for i in range(N)) == 1

# Subtour elimination constraints
for i in range(N):
    for j in range(N):
        if i != j and i != start_city and j != start_city:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1

# Solve the problem
problem.solve()

# Output the results
visit_order = []
total_distance = pulp.value(problem.objective)

for i in range(N):
    for j in range(N):
        if pulp.value(x[i][j]) == 1:
            visit_order.append(j)

print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
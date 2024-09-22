import pulp
import json

# Load data from JSON format
data = json.loads('{"N": 6, "Distances": [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], "StartCity": 0}')

# Define parameters
N = data['N']
distances = data['Distances']
start_city = data['StartCity']
C = list(range(N))

# Define the problem
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (C, C), cat='Binary')

# Objective function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in C for j in C if i != j)

# Constraints
# Each city must be visited exactly once (except start city)
problem += pulp.lpSum(x[start_city][j] for j in C if j != start_city) == 1
problem += pulp.lpSum(x[j][start_city] for j in C if j != start_city) == 1

for j in C:
    if j != start_city:
        problem += pulp.lpSum(x[i][j] for i in C if i != j) == 1
        problem += pulp.lpSum(x[j][i] for i in C if i != j) == 1

# Subtour elimination constraints
u = pulp.LpVariable.dicts("u", C, lowBound=0, upBound=N-1, cat='Integer')

for i in C:
    for j in C:
        if i != j and i != start_city and j != start_city:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1

# Solve the problem
problem.solve()

# Extract the solution
visit_order = []
for i in C:
    for j in C:
        if pulp.value(x[i][j]) == 1:
            visit_order.append(j)

# Calculate the total distance
total_distance = pulp.value(problem.objective)

# Output results
print(f' (Visit Order): {visit_order}')
print(f' (Total Distance): <OBJ>{total_distance}</OBJ>')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
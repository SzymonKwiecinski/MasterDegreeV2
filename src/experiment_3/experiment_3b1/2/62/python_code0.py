import pulp
import json

# Data input
data = json.loads("{'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}")

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Problem definition
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(N + 1), range(N + 1)), cat='Binary')

# Objective Function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N + 1) for j in range(N + 1) if i != j)

# Constraints
# Each city must be visited exactly once
problem += pulp.lpSum(x[start_city][j] for j in range(1, N + 1)) == 1

for j in range(1, N + 1):
    problem += pulp.lpSum(x[i][j] for i in range(N + 1)) == 1

# The traveler must return to the starting city
problem += pulp.lpSum(x[j][start_city] for j in range(1, N + 1)) == 1

# Subtour elimination constraints (Miller-Tucker-Zemlin formulation)
for s in range(2, N + 1):
    for subset in itertools.combinations(range(1, N + 1), s):
        problem += pulp.lpSum(x[i][j] for i in subset for j in subset) <= len(subset) - 1

# Solve the problem
problem.solve()

# Get the visit order and total distance
visit_order = []
total_distance = pulp.value(problem.objective)

for i in range(N + 1):
    for j in range(N + 1):
        if pulp.value(x[i][j]) == 1:
            visit_order.append(j)

print(f' (Visit Order): {visit_order}')
print(f' (Total Distance): <OBJ>{total_distance}</OBJ>')
import pulp
import itertools

# Data input
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}
N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Problem
problem = pulp.LpProblem("TravelingSalesmanProblem", pulp.LpMinimize)

# Variables
x = pulp.LpVariable.dicts('x', (range(N), range(N)), cat='Binary')
u = pulp.LpVariable.dicts('u', range(N), 0, N-1, cat='Continuous')

# Objective
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N) if i != j)

# Constraints
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N) if i != j) == 1
    problem += pulp.lpSum(x[j][i] for j in range(N) if i != j) == 1

for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1

# Solve
problem.solve()

# Extracting the tour
tour = [start_city]
current_city = start_city
while len(tour) < N + 1:
    for j in range(N):
        if pulp.value(x[current_city][j]) == 1:
            tour.append(j)
            current_city = j
            break

# Calculate total distance
total_distance = sum(distances[tour[i]][tour[i+1]] for i in range(N))

# Output
output = {
    "visit_order": tour,
    "total_distance": total_distance
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
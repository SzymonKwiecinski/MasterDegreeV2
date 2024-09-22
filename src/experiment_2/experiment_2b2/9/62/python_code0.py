import pulp
import itertools

# Problem data from JSON input
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}

# Extract data
N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Create the problem
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts('x', ((i, j) for i in range(N) for j in range(N)), cat='Binary')
u = pulp.LpVariable.dicts('u', (i for i in range(N)), lowBound=0, cat='Continuous')

# Objective
problem += pulp.lpSum(distances[i][j] * x[i, j] for i in range(N) for j in range(N))

# Constraints
for i in range(N):
    problem += pulp.lpSum(x[i, j] for j in range(N) if j != i) == 1
    problem += pulp.lpSum(x[j, i] for j in range(N) if j != i) == 1

# Eliminate sub-tours
for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + N * x[i, j] <= N - 1

# Solve the problem
problem.solve()

# Extract the optimal tour
tour = []
current_city = start_city
visited = set([start_city])

while len(visited) < N:
    for j in range(N):
        if j != current_city and pulp.value(x[current_city, j]) == 1:
            tour.append(j)
            visited.add(j)
            current_city = j
            break

tour.append(start_city)  # Return to the start city

# Calculate the total distance
total_distance = sum(distances[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))

# Output the result in the required format
result = {
    "visit_order": [start_city] + tour,
    "total_distance": total_distance
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
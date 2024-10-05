import pulp
import itertools

# Extract the data from the provided JSON format
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Initialize the problem
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')
u = pulp.LpVariable.dicts("u", range(N), lowBound=0, upBound=N-1, cat='Integer')

# Objective function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N) if i != j)

# Constraints
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N) if i != j) == 1  # Each city is left exactly once

for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N) if i != j) == 1  # Each city is entered exactly once

for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1  # Subtour elimination

# Solve the problem
problem.solve()

# Retrieve the solution
route = [start_city]
current_city = start_city
for _ in range(N):
    for next_city in range(N):
        if pulp.value(x[current_city][next_city]) == 1:
            route.append(next_city)
            current_city = next_city
            break

# Add start_city again to complete the cycle
route.append(start_city)

# Calculate the total distance
total_distance = sum(distances[route[i]][route[i+1]] for i in range(len(route)-1))

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the result
output = {
    "visit_order": route,
    "total_distance": total_distance
}
print(output)
from pulp import LpProblem, LpVariable, lpSum, LpMinimize, LpBinary
import pulp

# Input data
data = {
    "N": 6,
    "Distances": [
        [0, 182, 70, 399, 56, 214],
        [182, 0, 255, 229, 132, 267],
        [70, 255, 0, 472, 127, 287],
        [399, 229, 472, 0, 356, 484],
        [56, 132, 127, 356, 0, 179],
        [214, 267, 287, 484, 179, 0]
    ],
    "StartCity": 0
}

# Extract data from JSON
N = data["N"]
distances = data["Distances"]
start_city = data["StartCity"]

# Problem declaration
problem = LpProblem("Traveling_Salesman_Problem", LpMinimize)

# Decision variables
x = LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat=LpBinary)
u = LpVariable.dicts("u", (i for i in range(N)), lowBound=0, cat='Continuous')

# Objective function: minimize the total travel distance
problem += lpSum(distances[i][j] * x[i, j] for i in range(N) for j in range(N))

# Constraints
# Each city must be left exactly once
for i in range(N):
    problem += lpSum(x[i, j] for j in range(N) if j != i) == 1

# Each city must be entered exactly once
for j in range(N):
    problem += lpSum(x[i, j] for i in range(N) if i != j) == 1

# Subtour elimination constraints
for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + N * x[i, j] <= N - 1

# The start city is visited first, so set u[start_city] to zero
problem += u[start_city] == 0

# Solve the problem
problem.solve()

# Extract the results
visit_order = [start_city]
current_city = start_city
while len(visit_order) < N + 1:
    next_city = next(j for j in range(N) if x[current_city, j].varValue == 1)
    visit_order.append(next_city)
    current_city = next_city

# Calculate the total distance
total_distance = pulp.value(problem.objective)

# Output result
output = {
    "visit_order": visit_order,
    "total_distance": total_distance
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp
import itertools
import json

# Problem data
data = json.loads('{"N": 6, "Distances": [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], "StartCity": 0}')

# Extracting data
N = data["N"]
Dist = data["Distances"]
start_city = data["StartCity"]

# Create a MILP problem
problem = pulp.LpProblem("Travelling_Salesman_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N) if i != j), cat='Binary')
u = pulp.LpVariable.dicts("u", (i for i in range(N)), lowBound=0, upBound=N-1, cat='Integer')

# Objective function
problem += pulp.lpSum(Dist[i][j] * x[i, j] for i in range(N) for j in range(N) if i != j)

# Add constraints
for i in range(N):
    problem += pulp.lpSum(x[i, j] for j in range(N) if i != j) == 1, f"Outflow_{i}"
    problem += pulp.lpSum(x[j, i] for j in range(N) if i != j) == 1, f"Inflow_{i}"

# Subtour elimination constraints
for i, j in itertools.combinations(range(N), 2):
    if i != start_city and j != start_city:
        problem += u[i] - u[j] + (N-1) * x[i, j] <= N - 2

# Solve the problem
problem.solve()

# Extract the route
visit_order = [start_city]
next_city = start_city
for _ in range(N):
    next_city = [j for j in range(N) if x[next_city, j].varValue == 1][0]
    visit_order.append(next_city)

total_distance = pulp.value(problem.objective)

# Output format
output = {
    "visit_order": visit_order,
    "total_distance": total_distance
}

print(f"{output}")
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
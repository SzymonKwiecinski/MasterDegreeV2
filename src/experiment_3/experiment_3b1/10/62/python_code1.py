import pulp
import json

# Data from the provided JSON
data = json.loads('{"N": 6, "Distances": [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], "StartCity": 0}')

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Create the problem
problem = pulp.LpProblem("TravelingSalesmanProblem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')
u = pulp.LpVariable.dicts("u", range(N), lowBound=0, cat='Integer')

# Objective function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N)), "TotalTravelDistance"

# Constraints
# Each town is visited exactly once
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N)) == 1, f"Visit_once_from_{i}"
    problem += pulp.lpSum(x[j][i] for j in range(N)) == 1, f"Visit_once_to_{i}"

# Subtour elimination constraints (Miller-Tucker-Zemlin formulation)
for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1, f"Subtour_elimination_{i}_{j}"

for i in range(1, N):
    problem += u[i] >= 1, f"U_constraint_{i}"

# Solve the problem
problem.solve()

# Output the visit order and total distance
visit_order = []
for i in range(N):
    for j in range(N):
        if pulp.value(x[i][j]) == 1:
            visit_order.append(j)

print(f'Visit order: {visit_order}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp
import json

# Given data in JSON format
data = json.loads("""
{
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
""")

# Parameters
N = data['N']
d = data['Distances']
start_city = data['StartCity']

# Create the model
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N+1) for j in range(N+1) if i != j), cat='Binary')
u = pulp.LpVariable.dicts("u", (i for i in range(1, N+1)), lowBound=1, upBound=N)

# Objective function
problem += pulp.lpSum(d[i][j] * x[i, j] for i in range(N+1) for j in range(N+1) if i != j)

# Constraints
# Each city must be visited exactly once
problem += pulp.lpSum(x[start_city, j] for j in range(1, N+1)) == 1

for i in range(1, N+1):
    problem += pulp.lpSum(x[i, j] for j in range(N+1) if i != j) == 1

# Return to the starting city
problem += pulp.lpSum(x[i, start_city] for i in range(1, N+1)) == 1

# Subtour elimination constraints
for i in range(1, N+1):
    for j in range(1, N+1):
        if i != j:
            problem += u[i] - u[j] + (N - 1) * x[i, j] <= N - 2

# Solve the problem
problem.solve()

# Output the results
visit_order = []
total_distance = pulp.value(problem.objective)

for i in range(N+1):
    for j in range(N+1):
        if pulp.value(x[i, j]) == 1:
            visit_order.append(j)

print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
print(f'Visit Order: {visit_order}')
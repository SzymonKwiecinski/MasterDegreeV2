import pulp
import json

# Given data in JSON format
data = json.loads("{'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}")

# Parameters
N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Problem definition
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')
u = pulp.LpVariable.dicts("u", range(N), lowBound=0, upBound=N-1)

# Objective function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N)), "Total_Distance"

# Constraints
# Each city must be visited exactly once from the start city
problem += pulp.lpSum(x[start_city][j] for j in range(N)) == 1

# Each city must be left exactly once
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N)) == 1

# Each city must be entered exactly once
for i in range(N):
    problem += pulp.lpSum(x[j][i] for j in range(N)) == 1

# Eliminate sub-tours
for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1

# Solve the problem
problem.solve()

# Retrieve results
visit_order = []
total_distance = pulp.value(problem.objective)

for i in range(N):
    for j in range(N):
        if pulp.value(x[i][j]) == 1:
            visit_order.append(j)

# Output the visit order and total distance
print(f' (Visit Order): {visit_order}')
print(f' (Total Distance): <OBJ>{total_distance}</OBJ>')
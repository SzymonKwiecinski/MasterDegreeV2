import pulp
import json

# Data in JSON format
data = json.loads("{'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}")

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Define the problem
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(N + 1), range(N + 1)), cat='Binary')
u = pulp.LpVariable.dicts("u", range(1, N + 1), lowBound=1, cat='Continuous')

# Objective Function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N + 1) for j in range(N + 1))

# Constraints
# Each city must be entered and exited exactly once
problem += pulp.lpSum(x[start_city][j] for j in range(1, N + 1)) == 1
for i in range(1, N + 1):
    problem += pulp.lpSum(x[i][j] for j in range(N + 1)) == 1

# The return to the start city
problem += pulp.lpSum(x[i][start_city] for i in range(1, N + 1)) == 1

# Subtour elimination constraints
for i in range(1, N + 1):
    for j in range(1, N + 1):
        if i != j:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1

# Solve the problem
problem.solve()

# Retrieve the visit order 
visit_order = [start_city]
for i in range(N):
    for j in range(N + 1):
        if pulp.value(x[visit_order[-1]][j]) == 1:
            visit_order.append(j)
            break
visit_order.append(start_city)

# Output results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Visit Order: {visit_order}')
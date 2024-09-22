import pulp
import json

# Data provided in JSON format
data = json.loads("{'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}")

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Initialize the problem
problem = pulp.LpProblem("TravelingSalesmanProblem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts('x', (range(N), range(N)), lowBound=0, upBound=1, cat='Integer')
u = pulp.LpVariable.dicts('u', range(N), lowBound=2, upBound=N, cat='Continuous')

# Objective function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N) if i != j)

# Constraints
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N) if j != i) == 1, f"Leave_once_{i}"

for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N) if i != j) == 1, f"Arrive_once_{j}"

for i in range(2, N):
    for j in range(2, N):
        if i != j:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1, f"Subtour_elimination_{i}_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp
import json

# Input data
data = json.loads('{"N": 6, "Distances": [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], "StartCity": 0}')

# Parameters
N = data['N']
Distances = data['Distances']
start_city = data['StartCity']

# Create the problem
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), 0, 1, pulp.LpBinary)
u = pulp.LpVariable.dicts("u", range(N), lowBound=1)

# Objective Function
problem += pulp.lpSum(Distances[i][j] * x[i][j] for i in range(N) for j in range(N)), "Total_Travel_Distance"

# Constraints
# Every city is left exactly once
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N) if j != i) == 1, f"Leave_Once_{i}"

# Every city is entered exactly once
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N) if i != j) == 1, f"Enter_Once_{j}"

# Subtour elimination
for i in range(N):
    for j in range(N):
        if i != j:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1, f"Subtour_{i}_{j}"

# Auxiliary variable constraints
for i in range(N):
    problem += u[i] >= 1, f"Lower_Bound_{i}"
problem += u[start_city] == 0, "Start_City_Constraint"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
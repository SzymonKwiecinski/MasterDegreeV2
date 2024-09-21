import pulp
import json

# Given data in JSON format
data = json.loads("{'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}")

N = data['N']
Distances = data['Distances']
StartCity = data['StartCity']

# Problem definition
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts('x', ((i, j) for i in range(N) for j in range(N)), cat='Binary')
u = pulp.LpVariable.dicts('u', range(N), lowBound=1, upBound=N-1)

# Objective function
problem += pulp.lpSum(Distances[i][j] * x[i, j] for i in range(N) for j in range(N)), "Total_Travel_Distance"

# Constraints
# Each town must be visited exactly once
for i in range(N):
    problem += pulp.lpSum(x[i, j] for j in range(N) if j != i) == 1, f"Visit_Once_{i}"
    problem += pulp.lpSum(x[j, i] for j in range(N) if j != i) == 1, f"Leave_Once_{i}"

# Must return to the StartCity after visiting all other towns
problem += pulp.lpSum(x[StartCity, j] for j in range(N) if j != StartCity) == 1, "Return_Once_Start"
problem += pulp.lpSum(x[i, StartCity] for i in range(N) if i != StartCity) == 1, "Leave_Once_Start"

# Eliminate subtours
for i in range(2, N):
    for j in range(2, N):
        if i != j:
            problem += u[i] - u[j] + N * x[i, j] <= N - 1, f"Subtour_Elimination_{i}_{j}"

# Ensuring u_i is within the bounds
for i in range(2, N):
    problem += u[i] >= 1
    problem += u[i] <= N - 1

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp
import json

# Load data from the provided JSON format
data = json.loads("{'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}")

N = data['N']
Distances = data['Distances']
StartCity = data['StartCity']

# Create the problem
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(N) for j in range(N)), cat='Binary')
u = pulp.LpVariable.dicts("u", range(2, N+1), lowBound=1, upBound=N-1)

# Objective function
problem += pulp.lpSum(Distances[i][j] * x[(i, j)] for i in range(N) for j in range(N)), "Total_Travel_Distance"

# Constraints
# Each town must be visited exactly once
for i in range(N):
    problem += pulp.lpSum(x[(i, j)] for j in range(N) if j != i) == 1, f"Visit_Once_{i}"

for j in range(N):
    problem += pulp.lpSum(x[(i, j)] for i in range(N) if i != j) == 1, f"Leave_Once_{j}"

# StartCity must be visited and returned
problem += pulp.lpSum(x[(StartCity, j)] for j in range(N) if j != StartCity) == 1, "Leave_StartCity"
problem += pulp.lpSum(x[(i, StartCity)] for i in range(N) if i != StartCity) == 1, "Return_to_StartCity"

# Subtour elimination
for i in range(2, N+1):
    for j in range(2, N+1):
        if i != j:
            problem += u[i] - u[j] + N * x[(i-1, j-1)] <= N - 1, f"Subtour_Elim_{i}_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
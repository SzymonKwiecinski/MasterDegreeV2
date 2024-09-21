import pulp
import json

# Data provided in JSON format
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], 
                                [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], 
                                [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 
        'StartCity': 0}

# Problem definition
N = data['N']
Distances = data['Distances']
StartCity = data['StartCity']

# Create a linear programming problem
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')
u = pulp.LpVariable.dicts("u", range(1, N), lowBound=1, upBound=N-1)

# Objective Function
problem += pulp.lpSum(Distances[i][j] * x[i][j] for i in range(N) for j in range(N)), "Total_Distance"

# Constraints
# Each town must be visited exactly once
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N) if j != i) == 1, f"Visit_once_{i}"
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N) if i != j) == 1, f"Leave_once_{j}"

# Return to StartCity
problem += pulp.lpSum(x[StartCity][j] for j in range(N) if j != StartCity) == 1, "Leave_StartCity"
problem += pulp.lpSum(x[i][StartCity] for i in range(N) if i != StartCity) == 1, "Return_StartCity"

# Eliminate subtours
for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1, f"Subtour_elimination_{i}_{j}"

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
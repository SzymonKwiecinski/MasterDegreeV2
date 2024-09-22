import pulp
import json

# Data provided in JSON format
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], 
                               [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], 
                               [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 
        'StartCity': 0}

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Create the linear programming problem
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision variables
C = list(range(N))  # cities from 0 to N-1
x = pulp.LpVariable.dicts("x", (C, C), cat='Binary')
u = pulp.LpVariable.dicts("u", range(1, N), lowBound=0, upBound=N-1)

# Objective Function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in C for j in C if i != j), "TotalDistance"

# Constraints
# Departure from start city
problem += pulp.lpSum(x[start_city][j] for j in C if j != start_city) == 1, "DepartureFromStartCity"

# Exactly one departure from each town (except the starting city)
for i in range(1, N):
    problem += pulp.lpSum(x[i][j] for j in C if j != i) == 1, f"DepartureFromTown_{i}"

# Exactly one arrival to each town (except the starting city)
for j in range(1, N):
    problem += pulp.lpSum(x[i][j] for i in C if i != j) == 1, f"ArrivalToTown_{j}"

# Subtour elimination constraints
for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + (N * x[i][j]) <= N - 1, f"SubtourElimination_{i}_{j}"

# Solve the problem
problem.solve()

# Extract the results
visit_order = []
for i in C:
    for j in C:
        if pulp.value(x[i][j]) == 1:
            visit_order.append(j)

total_distance = pulp.value(problem.objective)

# Output the results
print(f' (Visit Order): {visit_order}')
print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
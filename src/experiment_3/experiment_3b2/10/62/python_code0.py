import json
import pulp

# Data from JSON
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], 
                               [182, 0, 255, 229, 132, 267], 
                               [70, 255, 0, 472, 127, 287], 
                               [399, 229, 472, 0, 356, 484], 
                               [56, 132, 127, 356, 0, 179], 
                               [214, 267, 287, 484, 179, 0]], 
        'StartCity': 0}

N = data['N']
distances = data['Distances']
C = range(1, N + 1)  # Set of cities {1, 2, ..., N}

# Define the problem
problem = pulp.LpProblem("TSP", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (C + (0,), C + (0,)), cat='Binary')
u = pulp.LpVariable.dicts("u", C, lowBound=1, cat='Continuous')

# Objective Function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in (C + (0,)) for j in (C + (0,)) if i != j), "Total_Distance"

# Constraints
# Leave start city exactly once
problem += pulp.lpSum(x[0][j] for j in C) == 1, "Leave_Start_City"
# Return to start city exactly once
problem += pulp.lpSum(x[i][0] for i in C) == 1, "Return_to_Start_City"

# Exactly one outgoing arc per city
for i in C:
    problem += pulp.lpSum(x[i][j] for j in (C + (0,)) if j != i) == 1, f"One_Outgoing_{i}"

# Exactly one incoming arc per city
for j in C:
    problem += pulp.lpSum(x[i][j] for i in (C + (0,)) if i != j) == 1, f"One_Incoming_{j}"

# Subtour elimination constraints
for i in C:
    for j in C:
        if i != j:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1, f"Subtour_{i}_{j}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
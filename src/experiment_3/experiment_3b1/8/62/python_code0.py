import pulp
import json

# Given data
data = json.loads("{'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}")

N = data['N']
C = list(range(N + 1))  # Cities from 0 to N
Distances = data['Distances']
start_city = data['StartCity']

# Create the problem
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts('x', (C, C), 0, 1, pulp.LpBinary)
u = pulp.LpVariable.dicts('u', range(1, N + 1), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(Distances[i][j] * x[i][j] for i in C for j in C), "Total_Distance"

# Constraints
# Each city is visited exactly once
problem += pulp.lpSum(x[start_city][j] for j in C) == 1, "Start_Visit_Once"

for j in range(1, N + 1):
    problem += pulp.lpSum(x[i][j] for i in C) == 1, f"Visit_Once_{j}"

problem += pulp.lpSum(x[j][start_city] for j in C) == 1, "Return_To_Start"

# Subtour elimination constraints
for i in range(1, N + 1):
    for j in range(1, N + 1):
        if i != j:
            problem += u[i] - u[j] + N * x[i][j] <= N - 1, f"Subtour_Elimination_{i}_{j}"

# Solve the problem
problem.solve()

# Extract the visit order and total distance
visit_order = []
total_distance = pulp.value(problem.objective)

# Get the sequence of towns visited
current_city = start_city
while len(visit_order) < N:
    for j in C:
        if pulp.value(x[current_city][j]) == 1:
            visit_order.append(j)
            current_city = j
            break

# Print results
print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
print(f'Visit Order: {visit_order}')
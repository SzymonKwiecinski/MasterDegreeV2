import pulp
import json

# Input data
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267],
                               [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484],
                               [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 
        'StartCity': 0}

# Extracting information from the data
N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Create the problem variable
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')
u = pulp.LpVariable.dicts("u", range(N), lowBound=0, upBound=N-1, cat='Integer')

# Objective function: minimize total distance
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N) if i != j)

# Constraints
# Each city must be left once
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N) if i != j) == 1

# Each city must be entered once
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N) if i != j) == 1

# Subtour elimination constraints
for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + (N-1) * x[i][j] <= N-2

# Starting point constraints
for j in range(1, N):
    problem += x[start_city][j] == 1
for j in range(1, N):
    problem += x[j][start_city] == 1

# Solve the problem
problem.solve()

# Extract the visit order and total distance from the solution
visit_order = []
current_city = start_city
visit_order.append(current_city)

while len(visit_order) < N + 1:
    for j in range(N):
        if x[current_city][j].value() == 1:
            visit_order.append(j)
            current_city = j
            break

# Append start city to complete the cycle
visit_order.append(start_city)

total_distance = pulp.value(problem.objective)

# Output formatting
output = {
    "visit_order": visit_order,
    "total_distance": total_distance
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
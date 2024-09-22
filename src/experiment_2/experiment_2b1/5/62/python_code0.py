import pulp
import numpy as np

# Input data
data = {
    'N': 6,
    'Distances': [[0, 182, 70, 399, 56, 214],
                  [182, 0, 255, 229, 132, 267],
                  [70, 255, 0, 472, 127, 287],
                  [399, 229, 472, 0, 356, 484],
                  [56, 132, 127, 356, 0, 179],
                  [214, 267, 287, 484, 179, 0]],
    'StartCity': 0
}

N = data['N']
Distances = np.array(data['Distances'])
start_city = data['StartCity']

# Create the problem instance
problem = pulp.LpProblem("Traveling_Salesman", pulp.LpMinimize)

# Create decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')

# Objective function: minimize the total distance
problem += pulp.lpSum(Distances[i][j] * x[i][j] for i in range(N) for j in range(N) if i != j)

# Constraints
# Each city must be entered and exited exactly once
for k in range(N):
    problem += pulp.lpSum(x[k][j] for j in range(N) if j != k) == 1  # Leave each city once
    problem += pulp.lpSum(x[i][k] for i in range(N) if i != k) == 1  # Enter each city once

# Subtour elimination constraints
u = pulp.LpVariable.dicts("u", range(N), lowBound=0, upBound=N-1, cat='Integer')
for i in range(1, N):
    for j in range(1, N):
        if i != j:
            problem += u[i] - u[j] + (N-1) * x[i][j] <= N - 2

# Solve the problem
problem.solve()

# Extract the visit order
visit_order = []
current_city = start_city
visit_order.append(current_city)

while len(visit_order) < N + 1:
    for j in range(N):
        if j != current_city and pulp.value(x[current_city][j]) == 1:
            visit_order.append(j)
            current_city = j
            break
visit_order.append(start_city)  # Returning to the start city

# Total distance traveled
total_distance = pulp.value(problem.objective)

# Output results
output = {
    "visit_order": visit_order,
    "total_distance": total_distance
}

# Printing the objective value
print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
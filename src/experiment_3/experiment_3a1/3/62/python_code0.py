import pulp
import numpy as np

# Data from the provided JSON
data = {
    'N': 6,
    'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267],
                  [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484],
                  [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]],
    'StartCity': 0
}

N = data['N']
distances = np.array(data['Distances'])
start_city = data['StartCity']

# Create the problem
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(N), range(N)), cat='Binary')

# Objective Function
problem += pulp.lpSum(distances[i][j] * x[i][j] for i in range(N) for j in range(N)), "Total_Distance"

# Constraints
# Each city must be visited exactly once
for i in range(N):
    problem += pulp.lpSum(x[i][j] for j in range(N) if j != i) == 1, f"Leave_City_{i}"

# Each city must be left exactly once
for j in range(N):
    problem += pulp.lpSum(x[i][j] for i in range(N) if i != j) == 1, f"Enter_City_{j}"

# Return to start city constraint
problem += pulp.lpSum(x[start_city][j] for j in range(N) if j != start_city) == 1, "Leave_Start_City"

# Solve the problem
problem.solve()

# Constructing the output
visit_order = []
total_distance = pulp.value(problem.objective)

current_city = start_city
visit_order.append(current_city)

while len(visit_order) < N:
    for j in range(N):
        if j != current_city and pulp.value(x[current_city][j]) == 1:
            visit_order.append(j)
            current_city = j
            break
visit_order.append(start_city)  # Return to start city

# Output the results
print(f'{{"visit_order": {visit_order}, "total_distance": {total_distance}}}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
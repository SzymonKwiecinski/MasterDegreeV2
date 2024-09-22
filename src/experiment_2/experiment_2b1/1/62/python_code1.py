import pulp
import numpy as np
import itertools  # Import itertools to use combinations

# Input data
data = {'N': 6, 'Distances': [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], 'StartCity': 0}

# Problem setup
N = data['N']
distances = np.array(data['Distances'])
start_city = data['StartCity']

# Create the problem
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

# Decision variables
routes = pulp.LpVariable.dicts("route", (range(N), range(N)), cat='Binary')

# Objective function
problem += pulp.lpSum(distances[i][j] * routes[i][j] for i in range(N) for j in range(N) if i != j)

# Constraints
# Each city must be left once
for j in range(N):
    problem += pulp.lpSum(routes[i][j] for i in range(N) if i != j) == 1
    
# Each city must be entered once
for i in range(N):
    problem += pulp.lpSum(routes[i][j] for j in range(N) if i != j) == 1

# Subtour elimination
for k in range(2, N):
    for subset in itertools.combinations(range(N), k):
        problem += pulp.lpSum(routes[i][j] for i in subset for j in subset if i != j) <= k - 1

# Solve the problem
problem.solve()

# Extracting the visit order and total distance
visit_order = [start_city]
next_city = start_city
while len(visit_order) < N + 1:
    for j in range(N):
        if routes[next_city][j].varValue == 1:
            visit_order.append(j)
            next_city = j
            break
visit_order.append(start_city)  # return to start city
total_distance = pulp.value(problem.objective)

# Output result
output = {
    "visit_order": visit_order,
    "total_distance": total_distance
}

print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
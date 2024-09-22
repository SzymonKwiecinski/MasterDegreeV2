import pulp
import json

# Given the input data in JSON format
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

# Extracting information from the data
N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Create a linear programming problem
problem = pulp.LpProblem("TravelingSalesman", pulp.LpMinimize)

# Decision variables
cities = range(N)
routes = pulp.LpVariable.dicts("route", (cities, cities), cat='Binary')

# Objective function: Minimize the total distance traveled
problem += pulp.lpSum(distances[i][j] * routes[i][j] for i in cities for j in cities if i != j)

# Constraints
# Each city must be entered and left exactly once
for k in cities:
    problem += pulp.lpSum(routes[k][j] for j in cities if j != k) == 1
    problem += pulp.lpSum(routes[i][k] for i in cities if i != k) == 1

# Subtour elimination constraints using Miller-Tucker-Zemlin formulation
u = pulp.LpVariable.dicts("u", cities, lowBound=0, upBound=N - 1, cat='Integer')

for i in cities[1:]:
    for j in cities[1:]:
        if i != j:
            problem += u[i] - u[j] + (N - 1) * routes[i][j] <= N - 2

# The objective is to return back to the starting city
problem += pulp.lpSum(routes[start_city][j] for j in cities if j != start_city) == 1
problem += pulp.lpSum(routes[i][start_city] for i in cities if i != start_city) == 1

# Solve the problem
problem.solve()

# Extracting the visit order
visit_order = []
for i in cities:
    for j in cities:
        if i != j and pulp.value(routes[i][j]) == 1:
            visit_order.append(j)

# Include the start city at the beginning
visit_order = [start_city] + visit_order + [start_city]

# Calculate total distance
total_distance = pulp.value(problem.objective)

result = {
    "visit_order": visit_order,
    "total_distance": total_distance
}

print(result)
print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
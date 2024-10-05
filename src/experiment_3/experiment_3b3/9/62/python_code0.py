import pulp
import json

# Data
data_json = '{"N": 6, "Distances": [[0, 182, 70, 399, 56, 214], [182, 0, 255, 229, 132, 267], [70, 255, 0, 472, 127, 287], [399, 229, 472, 0, 356, 484], [56, 132, 127, 356, 0, 179], [214, 267, 287, 484, 179, 0]], "StartCity": 0}'
data = json.loads(data_json)

N = data['N']
distances = data['Distances']
start_city = data['StartCity']

# Problem
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", [(i, j) for i in range(N) for j in range(N)], cat='Binary')

# Objective Function
problem += pulp.lpSum(distances[i][j] * x[i, j] for i in range(N) for j in range(N))

# Constraints
# Each city is entered exactly once
problem += pulp.lpSum(x[start_city, j] for j in range(N) if j != start_city) == 1

# Each city is exited exactly once
for j in range(N):
    problem += pulp.lpSum(x[i, j] for i in range(N) if i != j) == 1

# Maintain the number of visits from each city
for i in range(N):
    if i != start_city:
        problem += (pulp.lpSum(x[i, j] for j in range(N) if j != i) - 
                    pulp.lpSum(x[j, i] for j in range(N) if j != i)) == 0

# Solve
problem.solve()

# Output
visit_order = []
for i in range(N):
    for j in range(N):
        if pulp.value(x[i, j]) == 1:
            visit_order.append((i, j))

print("Visit Order:", visit_order)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
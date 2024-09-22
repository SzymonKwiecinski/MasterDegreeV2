import pulp

# Data
data = {
    'N': 6,
    'Distances': [
        [0, 182, 70, 399, 56, 214],
        [182, 0, 255, 229, 132, 267],
        [70, 255, 0, 472, 127, 287],
        [399, 229, 472, 0, 356, 484],
        [56, 132, 127, 356, 0, 179],
        [214, 267, 287, 484, 179, 0]
    ],
    'StartCity': 0
}

# Initialize problem
problem = pulp.LpProblem("Traveling_Salesman_Problem", pulp.LpMinimize)

# Sets and Parameters
N = data['N']
distances = data['Distances']
start_city = data['StartCity']
cities = list(range(N))

# Decision Variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in cities for j in cities), cat="Binary")

# Objective Function
problem += pulp.lpSum(distances[i][j] * x[i, j] for i in cities for j in cities), "Total Distance"

# Constraints
# 1. From start city to one town
problem += pulp.lpSum(x[start_city, j] for j in cities) == 1

# 2. Return to start city
problem += pulp.lpSum(x[j, start_city] for j in cities) == 1

# 3. Each town is visited exactly once
for i in cities:
    if i != start_city:
        problem += pulp.lpSum(x[i, j] for j in cities) == 1

# 4. Each town is left exactly once
for j in cities:
    if j != start_city:
        problem += pulp.lpSum(x[i, j] for i in cities) == 1

# Solve the problem
problem.solve()

# Output Results
visit_order = []
current_city = start_city
visited = set()
visited.add(current_city)

for _ in range(N-1):
    for j in cities:
        if j not in visited and pulp.value(x[current_city, j]) == 1:
            visit_order.append(j)
            visited.add(j)
            current_city = j
            break

total_distance = pulp.value(problem.objective)

# Print Objective
print(f'(Objective Value): <OBJ>{total_distance}</OBJ>')
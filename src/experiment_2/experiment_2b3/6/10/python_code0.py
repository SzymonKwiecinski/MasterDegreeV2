import pulp

# Input data
data = {
    'S': 3,
    'G': 2,
    'N': 4,
    'Capacity': [[15, 20], [20, 15], [5, 17]],
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]],
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

# Problem definition
problem = pulp.LpProblem("School_District_Assignment", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts(
    "x",
    ((n, s, g) for n in range(data['N']) for s in range(data['S']) for g in range(data['G'])),
    lowBound=0
)

# Objective function: Minimize total distance
problem += pulp.lpSum(
    data['Distance'][n][s] * x[(n, s, g)]
    for n in range(data['N'])
    for s in range(data['S'])
    for g in range(data['G'])
)

# Constraints
# 1. Each grade in each neighborhood gets fully assigned to some schools
for n in range(data['N']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[(n, s, g)] for s in range(data['S'])) == data['Population'][n][g]

# 2. School capacity constraints
for s in range(data['S']):
    for g in range(data['G']):
        problem += pulp.lpSum(x[(n, s, g)] for n in range(data['N'])) <= data['Capacity'][s][g]

# Solve the problem
problem.solve()

# Output format
assignment = [[[pulp.value(x[(n, s, g)]) for g in range(data['G'])] for s in range(data['S'])] for n in range(data['N'])]
total_distance = pulp.value(problem.objective)

output = {
    "assignment": assignment,
    "total_distance": total_distance
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
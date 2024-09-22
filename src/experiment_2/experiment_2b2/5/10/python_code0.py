import pulp

# Extract data from the given JSON format
data = {
    'S': 3,
    'G': 2,
    'N': 4,
    'Capacity': [[15, 20], [20, 15], [5, 17]],
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]],
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

N, S, G = data['N'], data['S'], data['G']
capacity = data['Capacity']
population = data['Population']
distance = data['Distance']

# Initialize the linear program problem
problem = pulp.LpProblem("Minimize_Student_Travel_Distance", pulp.LpMinimize)

# Decision variables
x = [[[pulp.LpVariable(f'x_{n}_{s}_{g}', lowBound=0) for g in range(G)] for s in range(S)] for n in range(N)]

# Objective function: Minimize the total distance
problem += pulp.lpSum(distance[n][s] * x[n][s][g] for n in range(N) for s in range(S) for g in range(G))

# Constraints

# 1. Each school should not exceed its capacity for each grade
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for n in range(N)) <= capacity[s][g]

# 2. All students in each neighborhood and grade must be assigned to a school
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for s in range(S)) == population[n][g]

# Solve the problem
problem.solve()

# Extracting the results
assignment = [[[pulp.value(x[n][s][g]) for g in range(G)] for s in range(S)] for n in range(N)]
total_distance = pulp.value(problem.objective)

# Output the results in the specified format
output = {
    "assignment": assignment,
    "total_distance": total_distance
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
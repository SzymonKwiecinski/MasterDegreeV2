import pulp

# Data input
data = {'S': 3, 'G': 2, 'N': 4, 'Capacity': [[15, 20], [20, 15], [5, 17]], 'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]}

# Unpacking data
S, G, N = data['S'], data['G'], data['N']
capacity = data['Capacity']
population = data['Population']
distance = data['Distance']

# Problem setup
problem = pulp.LpProblem("Minimize_Total_Distance", pulp.LpMinimize)

# Decision variables
x_vars = [[[pulp.LpVariable(f'x_{n}_{s}_{g}', lowBound=0) for g in range(G)] for s in range(S)] for n in range(N)]

# Objective function
problem += pulp.lpSum(distance[n][s] * x_vars[n][s][g] for n in range(N) for s in range(S) for g in range(G))

# Constraints
# Capacity constraints
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x_vars[n][s][g] for n in range(N)) <= capacity[s][g]

# Population constraints
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x_vars[n][s][g] for s in range(S)) == population[n][g]

# Solving the problem
problem.solve()

# Output the results
assignment = [[[pulp.value(x_vars[n][s][g]) for g in range(G)] for s in range(S)] for n in range(N)]
total_distance = pulp.value(problem.objective)

# Formatting the output as required
output = {
    "assignment": assignment,
    "total_distance": total_distance
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
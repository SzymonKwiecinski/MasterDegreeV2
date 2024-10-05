import pulp

# Data input
data = {'S': 3, 'G': 2, 'N': 4, 'Capacity': [[15, 20], [20, 15], [5, 17]], 'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]}

S = data['S']
G = data['G']
N = data['N']
capacity = data['Capacity']
population = data['Population']
distance = data['Distance']

# Initialize the problem
problem = pulp.LpProblem("School_District_Assignment", pulp.LpMinimize)

# Decision variables: x[n][s][g] represents the number of students from neighborhood n sent to school s in grade g
x = [[[pulp.LpVariable(f'x_{n}_{s}_{g}', lowBound=0, cat='Continuous') for g in range(G)] for s in range(S)] for n in range(N)]

# Objective: Minimize total distance
problem += pulp.lpSum(distance[n][s] * x[n][s][g] for n in range(N) for s in range(S) for g in range(G))

# Constraints
# 1. Capacity constraint for each school and grade
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for n in range(N)) <= capacity[s][g]

# 2. Population constraint for each neighborhood and grade
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for s in range(S)) == population[n][g]

# Solve the problem
problem.solve()

# Collect the results
assignment = [[[pulp.value(x[n][s][g]) for g in range(G)] for s in range(S)] for n in range(N)]
total_distance = pulp.value(problem.objective)

# Output
output = {
    "assignment": assignment,
    "total_distance": total_distance
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp

# Data
data = {
    "S": 3,
    "G": 2,
    "N": 4,
    "Capacity": [[15, 20], [20, 15], [5, 17]],
    "Population": [[7, 19], [4, 12], [9, 2], [6, 8]],
    "Distance": [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

S = data['S']
G = data['G']
N = data['N']
Capacity = data['Capacity']
Population = data['Population']
Distance = data['Distance']

# Problem
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

# Decision variables
x = [[[pulp.LpVariable(f"x_{n}_{s}_{g}", lowBound=0) for g in range(G)] for s in range(S)] for n in range(N)]

# Objective function
problem += pulp.lpSum(x[n][s][g] * Distance[n][s] for n in range(N) for s in range(S) for g in range(G))

# Constraints
# Each school's capacity cannot be exceeded
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for n in range(N)) <= Capacity[s][g]

# All students must be assigned
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for s in range(S)) == Population[n][g]

# Solve problem
problem.solve()

# Extract solution
assignment = [[[pulp.value(x[n][s][g]) for g in range(G)] for s in range(S)] for n in range(N)]
total_distance = pulp.value(problem.objective)

# Output
output = {
    "assignment": assignment,
    "total_distance": total_distance
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
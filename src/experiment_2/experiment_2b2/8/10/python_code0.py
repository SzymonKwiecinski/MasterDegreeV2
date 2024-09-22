import pulp

data = {'S': 3, 'G': 2, 'N': 4, 'Capacity': [[15, 20], [20, 15], [5, 17]], 'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]}

# Parameters
S = data['S']  # Number of schools
G = data['G']  # Number of grades
N = data['N']  # Number of neighborhoods
capacity = data['Capacity']
population = data['Population']
distance = data['Distance']

# Problem
problem = pulp.LpProblem("SchoolAssignment", pulp.LpMinimize)

# Variables: x[n][s][g] represents the number of students from neighborhood n of grade g assigned to school s
x = [[[pulp.LpVariable(f'x_{n}_{s}_{g}', lowBound=0, cat='Continuous') for g in range(G)] for s in range(S)] for n in range(N)]

# Objective: Minimize total distance traveled by all students
problem += pulp.lpSum(x[n][s][g] * distance[n][s] for n in range(N) for s in range(S) for g in range(G))

# Constraints
# 1. Each neighborhood's grade population must be completely assigned
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for s in range(S)) == population[n][g]
        
# 2. School's capacity for each grade should not be exceeded
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for n in range(N)) <= capacity[s][g]

# Solve the problem
problem.solve()

# Collect results
assignment = [[[x[n][s][g].varValue for g in range(G)] for s in range(S)] for n in range(N)]
total_distance = pulp.value(problem.objective)

# Output format
output = {
    "assignment": assignment,
    "total_distance": total_distance
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
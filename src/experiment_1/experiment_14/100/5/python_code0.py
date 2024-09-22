import pulp

# Extract data from JSON
data = {
    'S': 3, 
    'G': 2, 
    'N': 4, 
    'Capacity': [[15, 20], [20, 15], [5, 17]], 
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

S = data['S']
G = data['G']
N = data['N']
Capacity = data['Capacity']
Population = data['Population']
Distance = data['Distance']

# Initialize the problem
problem = pulp.LpProblem("School Assignment", pulp.LpMinimize)

# Decision variables x_{n,g,s}
x = [[[pulp.LpVariable(f'x_{n}_{g}_{s}', lowBound=0, cat='Continuous') for s in range(S)] for g in range(G)] for n in range(N)]

# Objective function
problem += pulp.lpSum(Distance[n][s] * x[n][g][s] for n in range(N) for g in range(G) for s in range(S)), "Minimize Total Distance"

# Constraints

# 1. Total number of students from each student group g assigned from neighborhood n does not exceed the population
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][g][s] for s in range(S)) == Population[n][g], f'Population_constraint_{n}_{g}'

# 2. Total number of students from each student group g assigned to school s does not exceed the capacity
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n][g][s] for n in range(N)) <= Capacity[s][g], f'Capacity_constraint_{s}_{g}'

# Solve the problem
problem.solve()

# Objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
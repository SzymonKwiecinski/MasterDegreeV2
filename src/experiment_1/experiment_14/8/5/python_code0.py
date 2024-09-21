import pulp

# Data from JSON
data = {
    'S': 3, 
    'G': 2, 
    'N': 4, 
    'Capacity': [[15, 20], [20, 15], [5, 17]], 
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

# Extracting data
S = data['S']
G = data['G']
N = data['N']
Capacity = data['Capacity']
Population = data['Population']
Distance = data['Distance']

# Problem definition
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", 
                          ((n, g, s) for n in range(N) for g in range(G) for s in range(S)),
                          lowBound=0,
                          cat='Continuous')

# Objective function: Minimize total distance
problem += pulp.lpSum(Distance[n][s] * x[(n, g, s)] for n in range(N) for g in range(G) for s in range(S))

# Constraints
# 1. Population constraint
for n in range(N):
    for g in range(G):
        problem += (pulp.lpSum(x[(n, g, s)] for s in range(S)) <= Population[n][g], f"Pop_Constraint_{n}_{g}")

# 2. Capacity constraint
for s in range(S):
    for g in range(G):
        problem += (pulp.lpSum(x[(n, g, s)] for n in range(N)) <= Capacity[s][g], f"Cap_Constraint_{s}_{g}")

# 3. Each student is assigned to exactly one school
for n in range(N):
    for g in range(G):
        problem += (pulp.lpSum(x[(n, g, s)] for s in range(S)) == Population[n][g], f"Assign_Constraint_{n}_{g}")

# Solve the problem
problem.solve()

# Objective Value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp

# Data
data = {
    'S': 3,
    'G': 2,
    'N': 4,
    'Capacity': [
        [15, 20],
        [20, 15],
        [5, 17]
    ],
    'Population': [
        [7, 19],
        [4, 12],
        [9, 2],
        [6, 8]
    ],
    'Distance': [
        [5.2, 4.0, 3.1],
        [3.8, 5.5, 6.1],
        [4.2, 3.5, 5.0],
        [5.0, 4.1, 3.2]
    ]
}

# Indices
S = data['S']  # Total number of schools
G = data['G']  # Total number of student groups
N = data['N']  # Total number of neighborhoods

Capacity = data['Capacity']
Population = data['Population']
Distance = data['Distance']

# Problem
problem = pulp.LpProblem("School_Assignment", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts(
    "x", ((n, g, s) for n in range(N) for g in range(G) for s in range(S)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(Distance[n][s] * x[n, g, s] for n in range(N) for g in range(G) for s in range(S))

# Constraints
# 1. Population assignment constraint
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n, g, s] for s in range(S)) <= Population[n][g]
    
# 2. Capacity constraint
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n, g, s] for n in range(N)) <= Capacity[s][g]

# 3. Each student is assigned to exactly one school
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n, g, s] for s in range(S)) == Population[n][g]

# Solve the problem
problem.solve()

# Objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
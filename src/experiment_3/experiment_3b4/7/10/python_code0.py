import pulp

# Data
data = {
    'S': 3,
    'G': 2,
    'N': 4,
    'Capacity': [[15, 20], [20, 15], [5, 17]],
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]],
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

N = data['N']
S = data['S']
G = data['G']
capacity = data['Capacity']
population = data['Population']
distance = data['Distance']

# Initialize the problem
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((n, s, g) for n in range(N) for s in range(S) for g in range(G)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(distance[n][s] * x[n, s, g] for n in range(N) for s in range(S) for g in range(G))

# Capacity Constraints
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n, s, g] for n in range(N)) <= capacity[s][g], f"Capacity_Constraint_School_{s}_Grade_{g}"

# Population Constraints
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n, s, g] for s in range(S)) == population[n][g], f"Population_Constraint_Neighborhood_{n}_Grade_{g}"

# Solve the problem
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
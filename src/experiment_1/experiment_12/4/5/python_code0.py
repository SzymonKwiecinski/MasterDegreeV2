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

S = data['S']  # Total number of schools
G = data['G']  # Total number of student groups
N = data['N']  # Total number of neighborhoods
Capacity = data['Capacity']
Population = data['Population']
Distance = data['Distance']

# Initialize the problem
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((n, g, s) for n in range(N) for g in range(G) for s in range(S)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(Distance[n][s] * x[(n, g, s)] for n in range(N) for g in range(G) for s in range(S)), "Total_Distance"

# Constraints
# Constraint 1: Students assigned to each school from a neighborhood cannot exceed the population of that group in the neighborhood
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[(n, g, s)] for s in range(S)) <= Population[n][g], f"Population_constraint_n{n}_g{g}"

# Constraint 2: Students assigned to each school cannot exceed the school's capacity for that group
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[(n, g, s)] for n in range(N)) <= Capacity[s][g], f"Capacity_constraint_s{s}_g{g}"

# Constraint 3: Each student is assigned to exactly one school
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[(n, g, s)] for s in range(S)) == Population[n][g], f"Assignment_constraint_n{n}_g{g}"

# Solve the problem
problem.solve()

# Print the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
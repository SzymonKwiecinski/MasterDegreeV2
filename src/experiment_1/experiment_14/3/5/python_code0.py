import pulp

# Data from the JSON
data = {
    'S': 3,
    'G': 2,
    'N': 4,
    'Capacity': [[15, 20], [20, 15], [5, 17]],
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]],
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

# Extracting the data
S = data['S']
G = data['G']
N = data['N']
Capacity = data['Capacity']
Population = data['Population']
Distance = data['Distance']

# Create the Linear Programming problem
problem = pulp.LpProblem("School_Assignment", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((n, g, s) for n in range(N) for g in range(G) for s in range(S)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(Distance[n][s] * x[(n, g, s)] for n in range(N) for g in range(G) for s in range(S))

# Constraints

# Constraint 1: Total number of students from each student group g assigned from neighborhood n to schools does not exceed the population of group g in neighborhood n
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[(n, g, s)] for s in range(S)) <= Population[n][g], f"Pop_Constraint_{n}_{g}"

# Constraint 2: Total number of students from each student group g assigned to school s does not exceed the capacity of school s for student group g
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[(n, g, s)] for n in range(N)) <= Capacity[s][g], f"Cap_Constraint_{s}_{g}"

# Constraint 3: Each student is assigned to exactly one school
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[(n, g, s)] for s in range(S)) == Population[n][g], f"Assign_Constraint_{n}_{g}"

# Constraint 4: All populations, capacities, and distances are non-negative
# (This is naturally enforced by the lowBound=0 in variable declaration)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
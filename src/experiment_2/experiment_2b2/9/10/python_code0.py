import pulp

# Data from the provided JSON
data = {
    'S': 3,
    'G': 2,
    'N': 4,
    'Capacity': [[15, 20], [20, 15], [5, 17]],
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]],
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

# Extract information
S = data['S']
G = data['G']
N = data['N']
Capacity = data['Capacity']
Population = data['Population']
Distance = data['Distance']

# Create the LP problem
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

# Decision variable x_{n,s,g}: students from neighborhood n to school s of grade g
x = pulp.LpVariable.dicts("x", ((n, s, g) for n in range(N) for s in range(S) for g in range(G)), lowBound=0, cat='Continuous')

# Objective: Minimize the total distance traveled by all students
problem += pulp.lpSum(Distance[n][s] * x[(n, s, g)] for n in range(N) for s in range(S) for g in range(G))

# Constraints
# Each neighborhood must assign all its students of each grade
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[(n, s, g)] for s in range(S)) == Population[n][g], f"Population_constraint_{n}_{g}"

# Each school must not exceed its capacity for each grade
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[(n, s, g)] for n in range(N)) <= Capacity[s][g], f"Capacity_constraint_{s}_{g}"

# Solve the problem
problem.solve()

# Prepare the output
assignment = [[[pulp.value(x[(n, s, g)]) for g in range(G)] for s in range(S)] for n in range(N)]
total_distance = pulp.value(problem.objective)

output = {
    "assignment": assignment,
    "total_distance": total_distance
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
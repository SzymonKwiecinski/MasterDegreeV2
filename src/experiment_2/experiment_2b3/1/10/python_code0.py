import pulp

# Extracting data from the JSON format
data = {
    'S': 3, 
    'G': 2, 
    'N': 4, 
    'Capacity': [[15, 20], [20, 15], [5, 17]], 
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

# Extract variables from data
S = data['S']
G = data['G']
N = data['N']
capacity = data['Capacity']
population = data['Population']
distance = data['Distance']

# Problem
problem = pulp.LpProblem("AssignStudentsToSchools", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((n, s, g) for n in range(N) for s in range(S) for g in range(G)), lowBound=0, cat=pulp.LpContinuous)

# Objective function: Minimize the total distance
problem += pulp.lpSum(distance[n][s] * x[n, s, g] for n in range(N) for s in range(S) for g in range(G))

# Constraints

# 1. Each neighborhood's students in each grade are assigned to schools.
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n, s, g] for s in range(S)) == population[n][g], f"Population_assigned_n{n}_g{g}"

# 2. Each school's capacity for each grade is not exceeded.
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n, s, g] for n in range(N)) <= capacity[s][g], f"Capacity_s{s}_g{g}"

# Solve the problem
problem.solve()

# Collecting the results
assignment = [[[pulp.value(x[n, s, g]) for g in range(G)] for s in range(S)] for n in range(N)]
total_distance = pulp.value(problem.objective)

# Output format
output = {
    "assignment": assignment,
    "total_distance": total_distance
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
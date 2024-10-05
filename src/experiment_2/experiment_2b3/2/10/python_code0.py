import pulp

# Problem definition
problem = pulp.LpProblem("School_Assignment", pulp.LpMinimize)

# Data
data = {'S': 3, 'G': 2, 'N': 4, 'Capacity': [[15, 20], [20, 15], [5, 17]], 'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]}

S = data['S']
G = data['G']
N = data['N']
capacities = data['Capacity']
populations = data['Population']
distances = data['Distance']

# Decision variables
x = pulp.LpVariable.dicts("x", ((n, s, g) for n in range(N) for s in range(S) for g in range(G)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(distances[n][s] * x[n, s, g] for n in range(N) for s in range(S) for g in range(G)), "Total_Distance"

# Constraints

# Each grade in each neighborhood must be completely assigned to schools
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n, s, g] for s in range(S)) == populations[n][g], f"Assign_All_Students_n{n}_g{g}"

# Schools' capacity constraints
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n, s, g] for n in range(N)) <= capacities[s][g], f"Capacity_s{s}_g{g}"

# Solve the problem
problem.solve()

# Extract results
assignment = [[[pulp.value(x[n, s, g]) for g in range(G)] for s in range(S)] for n in range(N)]
total_distance = pulp.value(problem.objective)

# Output format
output = {
    "assignment": assignment,
    "total_distance": total_distance
}

import json
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
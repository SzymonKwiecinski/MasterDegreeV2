import pulp
import json

data = {'S': 3, 'G': 2, 'N': 4, 'Capacity': [[15, 20], [20, 15], [5, 17]], 'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]}

S = data['S']
G = data['G']
N = data['N']
capacity = data['Capacity']
population = data['Population']
distance = data['Distance']

# Create the problem
problem = pulp.LpProblem("SchoolAssignment", pulp.LpMinimize)

# Decision variables: x[n][s][g] for number of students from neighborhood n assigned to school s for grade g
x = pulp.LpVariable.dicts("x", ((n, s, g) for n in range(N) for s in range(S) for g in range(G)), lowBound=0)

# Objective function: Minimize total distance
problem += pulp.lpSum(x[n, s, g] * distance[n][s] for n in range(N) for s in range(S) for g in range(G)), "TotalDistance"

# Constraints: Fulfill the capacity constraints
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n, s, g] for n in range(N)) <= capacity[s][g], f"CapacityConstraint_s{s}_g{g}"

# Constraints: Fulfill the population requirements
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n, s, g] for s in range(S)) == population[n][g], f"PopulationConstraint_n{n}_g{g}"

# Solve the problem
problem.solve()

# Prepare output
assignment = [[[0 for g in range(G)] for s in range(S)] for n in range(N)]
for n in range(N):
    for s in range(S):
        for g in range(G):
            assignment[n][s][g] = pulp.value(x[n, s, g])

total_distance = pulp.value(problem.objective)

# Output
output = {
    "assignment": assignment,
    "total_distance": total_distance
}

print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
print(json.dumps(output, indent=4))
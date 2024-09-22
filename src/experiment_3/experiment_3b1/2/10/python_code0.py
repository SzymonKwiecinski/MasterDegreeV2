import pulp
import json

# Data input
data = json.loads("{'S': 3, 'G': 2, 'N': 4, 'Capacity': [[15, 20], [20, 15], [5, 17]], 'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]}")

# Problem variables
N = data['N']
S = data['S']
G = data['G']
capacity = data['Capacity']
population = data['Population']
distance = data['Distance']

# LP problem
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(S), range(G)), lowBound=0, cat='Continuous')

# Objective function
problem += pulp.lpSum(distance[n][s] * x[n][s][g] for n in range(N) for s in range(S) for g in range(G)), "Total_Distance"

# Supply constraints
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for s in range(S)) == population[n][g], f"Supply_Constraint_n{n}_g{g}"

# Demand constraints
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for n in range(N)) <= capacity[s][g], f"Demand_Constraint_s{s}_g{g}"

# Solve the problem
problem.solve()

# Output results
assignment_matrix = [[[pulp.value(x[n][s][g]) for g in range(G)] for s in range(S)] for n in range(N)]

print("Assignment Matrix (students assigned):")
for n in range(N):
    for s in range(S):
        print(f"Neighborhood {n}, School {s}: {assignment_matrix[n][s]}")

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
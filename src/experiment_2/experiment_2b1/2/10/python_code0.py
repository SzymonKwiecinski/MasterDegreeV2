import pulp
import json

# Data from input
data = {
    'S': 3,
    'G': 2,
    'N': 4,
    'Capacity': [[15, 20], [20, 15], [5, 17]],
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]],
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

# Constants from data
N = data['N']
S = data['S']
G = data['G']
capacity = data['Capacity']
population = data['Population']
distance = data['Distance']

# Create the LP problem
problem = pulp.LpProblem("School_Assignment", pulp.LpMinimize)

# Decision variable x[n][s][g]: number of students of grade g in neighborhood n assigned to school s
x = pulp.LpVariable.dicts("x", (range(N), range(S), range(G)), lowBound=0)

# Objective function: Minimize total distance traveled by all students
problem += pulp.lpSum(x[n][s][g] * distance[n][s] for n in range(N) for s in range(S) for g in range(G)), "Total_Distance"

# Constraints:

# 1. Each neighborhood's student population must be fully assigned
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for s in range(S)) == population[n][g], f"Population_Constraint_n{n}_g{g}"

# 2. Each school's capacity must not be exceeded
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for n in range(N)) <= capacity[s][g], f"Capacity_Constraint_s{s}_g{g}"

# Solve the problem
problem.solve()

# Collect results
assignment = [[[pulp.value(x[n][s][g]) for g in range(G)] for s in range(S)] for n in range(N)]
total_distance = pulp.value(problem.objective)

# Output the result
output = {
    "assignment": assignment,
    "total_distance": total_distance
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
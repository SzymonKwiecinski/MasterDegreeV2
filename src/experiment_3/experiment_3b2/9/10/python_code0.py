import pulp
import json

# Input data in json format
data = json.loads('{"S": 3, "G": 2, "N": 4, "Capacity": [[15, 20], [20, 15], [5, 17]], "Population": [[7, 19], [4, 12], [9, 2], [6, 8]], "Distance": [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]}')

# Extracting data from JSON
S = data['S']  # Number of schools
G = data['G']  # Number of grades
N = data['N']  # Number of neighborhoods
capacity = data['Capacity']  # Capacity constraints
population = data['Population']  # Population requirements
distance = data['Distance']  # Distance matrix

# Create the problem
problem = pulp.LpProblem("Student_Assignment_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(S), range(G)), lowBound=0, cat='Continuous')

# Objective function: Minimize total distance
problem += pulp.lpSum(distance[n][s] * x[n][s][g] for n in range(N) for s in range(S) for g in range(G))

# Capacity constraints for each school and grade
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for n in range(N)) <= capacity[s][g], f"Capacity_Constraint_s{s}_g{g}"

# Population constraints for each neighborhood and grade
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for s in range(S)) == population[n][g], f"Population_Constraint_n{n}_g{g}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
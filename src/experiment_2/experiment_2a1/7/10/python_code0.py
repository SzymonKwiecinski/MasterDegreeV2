import pulp
import json

# Input data
data = {'S': 3, 'G': 2, 'N': 4, 'Capacity': [[15, 20], [20, 15], [5, 17]], 
        'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 
        'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]}

# Parameters
N = data['N']
S = data['S']
G = data['G']
capacity = data['Capacity']
population = data['Population']
distance = data['Distance']

# Define the problem
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("assignment", (range(N), range(S), range(G)), lowBound=0, cat='Continuous')

# Objective function: Minimize total distance traveled by all students
problem += pulp.lpSum(x[n][s][g] * distance[n][s] for n in range(N) for s in range(S) for g in range(G)), "Total_Distance"

# Constraints
# Capacity constraints
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for n in range(N)) <= capacity[s][g], f"Capacity_Constraint_s{S}_g{g}"

# Population constraints
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for s in range(S)) == population[n][g], f"Population_Constraint_n{n}_g{g}"

# Solve the problem
problem.solve()

# Prepare the output
assignment = [[[x[n][s][g].varValue for g in range(G)] for s in range(S)] for n in range(N)]
total_distance = pulp.value(problem.objective)

# Output as per required format
output = {
    "assignment": assignment,
    "total_distance": total_distance
}

# Print the objective value
print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
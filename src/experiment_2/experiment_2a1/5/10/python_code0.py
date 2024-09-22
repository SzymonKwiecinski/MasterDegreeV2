import pulp
import json

# Data input in JSON format
data = {
    'S': 3,
    'G': 2,
    'N': 4,
    'Capacity': [[15, 20], [20, 15], [5, 17]],
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]],
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

# Extract parameters
S = data['S']
G = data['G']
N = data['N']
capacity = data['Capacity']
population = data['Population']
distance = data['Distance']

# Create the linear programming problem
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

# Define decision variables
x = pulp.LpVariable.dicts("x", 
                           ((n, s, g) for n in range(N) for s in range(S) for g in range(G)), 
                           lowBound=0, 
                           cat='Continuous')

# Objective function: minimize total distance
problem += pulp.lpSum(x[n, s, g] * distance[n][s] for n in range(N) for s in range(S) for g in range(G)), "Total_Distance"

# Constraints: the number of students assigned to a school cannot exceed capacity
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n, s, g] for n in range(N)) <= capacity[s][g], f"Capacity_Constraint_School_{s}_Grade_{g}"

# Constraints: all students must be assigned
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n, s, g] for s in range(S)) == population[n][g], f"Population_Constraint_Neighborhood_{n}_Grade_{g}"

# Solve the problem
problem.solve()

# Prepare the output
assignment = [[[x[n, s, g].varValue for g in range(G)] for s in range(S)] for n in range(N)]
total_distance = pulp.value(problem.objective)

# Format and print the output
output = {
    "assignment": assignment,
    "total_distance": total_distance
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{total_distance}</OBJ>')
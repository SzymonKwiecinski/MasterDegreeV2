import pulp
import json

# Load data from the provided JSON format
data = {'S': 3, 'G': 2, 'N': 4, 
        'Capacity': [[15, 20], [20, 15], [5, 17]], 
        'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 
        'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]}

S = data['S']
G = data['G']
N = data['N']
capacity = data['Capacity']
population = data['Population']
distance = data['Distance']

# Create the problem
problem = pulp.LpProblem("School_Assignment", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", (range(N), range(S), range(G)), lowBound=0, cat='Continuous')

# Objective function: Minimize total distance
total_distance = pulp.lpSum(distance[n][s] * x[n][s][g] for n in range(N) for s in range(S) for g in range(G))
problem += total_distance

# Constraints
# 1. Ensure that the number of students assigned does not exceed the capacity
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for n in range(N)) <= capacity[s][g]

# 2. Ensure that all students are assigned
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for s in range(S)) == population[n][g]

# Solve the problem
problem.solve()

# Prepare the output
assignment = [[[x[n][s][g].varValue for g in range(G)] for s in range(S)] for n in range(N)]
total_distance_value = pulp.value(problem.objective)

output = {
    "assignment": assignment,
    "total_distance": total_distance_value
}

# Print the result
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp
import json

# Data from the user input
data = {
    'S': 3, 
    'G': 2, 
    'N': 4,
    'Capacity': [[15, 20], [20, 15], [5, 17]], 
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]], 
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

S = data['S']
G = data['G']
N = data['N']
capacity = data['Capacity']
population = data['Population']
distance = data['Distance']

# Create the LP problem
problem = pulp.LpProblem("School_Assignment", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((n, s, g) for n in range(N) for s in range(S) for g in range(G)), lowBound=0)

# Objective function: minimize total distance traveled
problem += pulp.lpSum(distance[n][s] * x[(n, s, g)] for n in range(N) for s in range(S) for g in range(G))

# Constraints
# 1. All students should be assigned
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[(n, s, g)] for s in range(S)) == population[n][g]

# 2. Cannot exceed school capacity
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[(n, s, g)] for n in range(N)) <= capacity[s][g]

# Solve the problem
problem.solve()

# Retrieve results
assignment = [[[x[(n, s, g)].varValue for g in range(G)] for s in range(S)] for n in range(N)]
total_distance = pulp.value(problem.objective)

# Output the results
output = {
    "assignment": assignment,
    "total_distance": total_distance
}

# Display the results
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
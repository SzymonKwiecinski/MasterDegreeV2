import pulp
import json

# Input data in json format
data = '''
{
    "S": 3, 
    "G": 2, 
    "N": 4, 
    "Capacity": [[15, 20], [20, 15], [5, 17]], 
    "Population": [[7, 19], [4, 12], [9, 2], [6, 8]], 
    "Distance": [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}
'''

# Load data as a dictionary
data = json.loads(data)

# Extracting data
S = data["S"]
G = data["G"]
N = data["N"]
capacities = data["Capacity"]
populations = data["Population"]
distances = data["Distance"]

# Initialize the problem
problem = pulp.LpProblem("School_Assignment", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((n, s, g) for n in range(N) for s in range(S) for g in range(G)), lowBound=0)

# Objective function
problem += pulp.lpSum(x[n, s, g] * distances[n][s] for n in range(N) for s in range(S) for g in range(G))

# Constraints
# Population constraints
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n, s, g] for s in range(S)) == populations[n][g]

# Capacity constraints
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n, s, g] for n in range(N)) <= capacities[s][g]

# Solve the problem
problem.solve()

# Extracting the results
assignment = [[[pulp.value(x[n, s, g]) for g in range(G)] for s in range(S)] for n in range(N)]
total_distance = pulp.value(problem.objective)

# Output
output = {
    "assignment": assignment,
    "total_distance": total_distance
}

print(json.dumps(output, indent=4))
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
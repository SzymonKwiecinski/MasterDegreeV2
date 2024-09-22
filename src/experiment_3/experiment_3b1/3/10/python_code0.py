import pulp
import json

# Data provided in the problem
data = {
    'S': 3,
    'G': 2,
    'N': 4,
    'Capacity': [[15, 20], [20, 15], [5, 17]],
    'Population': [[7, 19], [4, 12], [9, 2], [6, 8]],
    'Distance': [[5.2, 4.0, 3.1], [3.8, 5.5, 6.1], [4.2, 3.5, 5.0], [5.0, 4.1, 3.2]]
}

# Extracting parameters from the data
N = data['N']
S = data['S']
G = data['G']
capacity = data['Capacity']
population = data['Population']
distance = data['Distance']

# Create a LP problem
problem = pulp.LpProblem("School_Assignment_Problem", pulp.LpMinimize)

# Decision Variables: x[n, s, g]
x = pulp.LpVariable.dicts("x", (range(N), range(S), range(G)), lowBound=0, cat='Continuous')

# Objective Function
problem += pulp.lpSum(distance[n][s] * x[n][s][g] for n in range(N) for s in range(S) for g in range(G)), "Total_Distance"

# Capacity Constraints
for s in range(S):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for n in range(N)) <= capacity[s][g], f"Capacity_Constraint_{s}_{g}"

# Demand Constraints
for n in range(N):
    for g in range(G):
        problem += pulp.lpSum(x[n][s][g] for s in range(S)) == population[n][g], f"Demand_Constraint_{n}_{g}"

# Solve the problem
problem.solve()

# Output the results
assignment = {}
for n in range(N):
    for s in range(S):
        for g in range(G):
            assignment[(n, s, g)] = x[n][s][g].varValue

print(f'Optimal Assignment: {assignment}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
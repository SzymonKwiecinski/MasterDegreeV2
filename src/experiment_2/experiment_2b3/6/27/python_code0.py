import pulp
import json

# Input data
data = json.loads('{"benefit": [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]], "communication": [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]], "cost": [[5, 14, 13], [15, 5, 9], [13, 9, 10]]}')

benefit = data['benefit']
communication = data['communication']
cost = data['cost']

K = len(benefit)  # Number of departments
L = len(benefit[0])  # Number of cities

# Defining the problem
problem = pulp.LpProblem("Relocation_Problem", pulp.LpMinimize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", ((k, l) for k in range(K) for l in range(L)), cat='Binary')

# Objective function
total_cost = 0
for k in range(K):
    for l in range(L):
        total_cost -= benefit[k][l] * islocated[k, l]
        for j in range(K):
            for m in range(L):
                total_cost += communication[k][j] * cost[l][m] * islocated[k, l] * islocated[j, m]

problem += total_cost

# Constraints
# Each department must be located in exactly one city
for k in range(K):
    problem += pulp.lpSum(islocated[k, l] for l in range(L)) == 1

# No more than three departments in each city
for l in range(L):
    problem += pulp.lpSum(islocated[k, l] for k in range(K)) <= 3

# Solve the problem
problem.solve()

# Prepare the output
output = {"islocated": [[int(islocated[k, l].varValue) for l in range(L)] for k in range(K)]}

# Print the output
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp
import json

data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]],
    'cost': [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}

K = len(data['benefit'])  # Number of departments
L = len(data['benefit'][0])  # Number of cities

# Create the problem variable
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", ((k, l) for k in range(K) for l in range(L)), cat='Binary')

# Objective function
benefit = data['benefit']
communication = data['communication']
cost = data['cost']

# Minimize overall yearly cost
problem += pulp.lpSum(benefit[k][l] * islocated[(k, l)] for k in range(K) for l in range(L)) + \
           pulp.lpSum(communication[k][j] * cost[l][m] * islocated[(k, l)] * islocated[(j, m)]
                      for k in range(K) for j in range(K) for l in range(L) for m in range(L))

# Constraints
# Each department must be located in one city
for k in range(K):
    problem += pulp.lpSum(islocated[(k, l)] for l in range(L)) == 1

# No more than three departments can be located in the same city
for l in range(L):
    problem += pulp.lpSum(islocated[(k, l)] for k in range(K)) <= 3

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
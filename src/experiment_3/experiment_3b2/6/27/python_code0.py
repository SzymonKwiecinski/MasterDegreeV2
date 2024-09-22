import pulp
import json

# Data input
data_json = """{'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]], 'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]], 'cost': [[5, 14, 13], [15, 5, 9], [13, 9, 10]]}"""
data = json.loads(data_json)

benefit = data['benefit']
communication = data['communication']
cost = data['cost']

K = len(benefit)  # Number of departments
L = len(cost)     # Number of cities

# Define the problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision Variables
islocated = pulp.LpVariable.dicts("islocated", (range(K), range(L)), cat='Binary')

# Objective Function
objective = pulp.lpSum(-benefit[k][l] * islocated[k][l] for k in range(K) for l in range(L)) + \
    pulp.lpSum(communication[k][j] * cost[l][m] * islocated[k][l] * islocated[j][m]
               for k in range(K) for j in range(K) for l in range(L) for m in range(L))

problem += objective

# Constraints
# Each department must be located in exactly one city
for k in range(K):
    problem += pulp.lpSum(islocated[k][l] for l in range(L)) == 1

# No city can host more than three departments
for l in range(L):
    problem += pulp.lpSum(islocated[k][l] for k in range(K)) <= 3

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
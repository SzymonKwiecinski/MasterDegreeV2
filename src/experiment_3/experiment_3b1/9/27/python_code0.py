import pulp
import json

# Input data
data = json.loads('{"benefit": [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]], "communication": [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]], "cost": [[5, 14, 13], [15, 5, 9], [13, 9, 10]]}')

# Parameters
benefit = data['benefit']
communication = data['communication']
cost = data['cost']
K = len(benefit)
L = len(cost)

# Problem
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision Variables
islocated = pulp.LpVariable.dicts("islocated", (range(K), range(L)), 0, 1, pulp.LpBinary)

# Objective Function
problem += pulp.lpSum(
    [pulp.lpSum(
        [communication[k][j] * cost[l][m] * islocated[k][l]
         for j in range(K) for m in range(L)]) 
     for l in range(L)]) - pulp.lpSum(
    [benefit[k][l] * islocated[k][l] for k in range(K) for l in range(L)])

# Constraints
# Department Location Constraint
for k in range(K):
    problem += pulp.lpSum(islocated[k][l] for l in range(L)) == 1

# City Capacity Constraint
for l in range(L):
    problem += pulp.lpSum(islocated[k][l] for k in range(K)) <= 3

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
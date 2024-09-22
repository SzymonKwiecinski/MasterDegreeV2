import pulp
import json

# Input data
data = {'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]], 
        'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], 
                          [0.0, 0.0, 1.4, 1.2, 0.0], 
                          [1.0, 1.4, 0.0, 0.0, 2.0], 
                          [1.5, 1.2, 0.0, 2.0, 0.7], 
                          [0.0, 0.0, 2.0, 0.7, 0.0]], 
        'cost': [[5, 14, 13], 
                 [15, 5, 9], 
                 [13, 9, 10]]}

benefit = data['benefit']
communication = data['communication']
cost = data['cost']

K = len(benefit)  # Number of departments
L = len(cost)  # Number of cities

# Create the problem
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", 
                                   ((k, l) for k in range(K) for l in range(L)), 
                                   cat='Binary')

# Objective function: Minimize total costs
problem += pulp.lpSum(communication[k][j] * cost[l][m] * islocated[(k, l)] for k in range(K) for l in range(L) for j in range(K) for m in range(L)) - pulp.lpSum(benefit[k][l] * islocated[(k, l)] for k in range(K) for l in range(L))

# Constraints
for k in range(K):
    problem += pulp.lpSum(islocated[(k, l)] for l in range(L)) <= 1  # Each department can only be located in one city

for l in range(L):
    problem += pulp.lpSum(islocated[(k, l)] for k in range(K)) <= 3  # No more than 3 departments can be located in the same city

# Solve the problem
problem.solve()

# Prepare the output
islocated_result = [[pulp.value(islocated[(k, l)]) for l in range(L)] for k in range(K)]

# Print the results
output = {
    "islocated": islocated_result
}
print(json.dumps(output))

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
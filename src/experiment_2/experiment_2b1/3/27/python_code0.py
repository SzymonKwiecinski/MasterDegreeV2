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

# Problem definition
K = len(data['benefit'])  # Number of departments
L = len(data['cost'])     # Number of cities (including London)

problem = pulp.LpProblem("Department_Location_Problem", pulp.LpMinimize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", (range(K), range(L)), cat='Binary')

# Objective function: Minimize total costs (benefits and communication costs)
total_cost = pulp.lpSum([
    -data['benefit'][k][l] * islocated[k][l] for k in range(K) for l in range(L)
]) + pulp.lpSum([
    data['communication'][k][j] * data['cost'][l][m] * islocated[k][l] * islocated[j][m]
    for k in range(K) for j in range(K) for l in range(L) for m in range(L)
])

problem += total_cost

# Constraints: Each department is located in one city
for k in range(K):
    problem += pulp.lpSum([islocated[k][l] for l in range(L)]) == 1

# Constraints: No more than 3 departments can be located in the same city
for l in range(L):
    problem += pulp.lpSum([islocated[k][l] for k in range(K)]) <= 3

# Solve the problem
problem.solve()

# Extracting results
islocated_result = [[int(islocated[k][l].value()) for l in range(L)] for k in range(K)]

# Preparing output
output = {
    "islocated": islocated_result,
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
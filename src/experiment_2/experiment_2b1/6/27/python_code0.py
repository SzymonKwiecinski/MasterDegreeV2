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

K = len(data['benefit'])  # Number of departments
L = len(data['benefit'][0])  # Number of possible cities

# Create the linear programming problem
problem = pulp.LpProblem("Department_Relocation_Optimization", pulp.LpMinimize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", (range(K), range(L)), cat='Binary')

# Objective function
total_cost = pulp.lpSum([
    (data['communication'][k][j] * data['cost'][l][m] * islocated[k][l] * islocated[j][m]) 
    for k in range(K) for l in range(L) for j in range(K) for m in range(L)
]) - pulp.lpSum([data['benefit'][k][l] * islocated[k][l] for k in range(K) for l in range(L)])

problem += total_cost

# Constraints for location limits
for l in range(L):
    problem += pulp.lpSum([islocated[k][l] for k in range(K)]) <= 3

# Constraint: each department must be located in exactly one city
for k in range(K):
    problem += pulp.lpSum([islocated[k][l] for l in range(L)]) == 1

# Solve the problem
problem.solve()

# Prepare the output
islocated_output = [[int(islocated[k][l].value()) for l in range(L)] for k in range(K)]

# Print results
print(json.dumps({"islocated": islocated_output}))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
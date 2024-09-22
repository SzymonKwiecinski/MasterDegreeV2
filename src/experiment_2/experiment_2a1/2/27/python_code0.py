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

# Problem setup
K = len(data['benefit'])  # Number of departments
L = len(data['cost'])     # Number of cities

problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", 
                                    ((k, l) for k in range(K) for l in range(L)),
                                    cat="Binary")

# Objective function: minimize total costs
total_cost = pulp.lpSum(
    (data['communication'][k][j] * data['cost'][l][m] * islocated[(k, l)]
     for k in range(K) for l in range(L) 
     for j in range(K) for m in range(L) 
     if j != m)  # Avoid communication in same city
) - pulp.lpSum(data['benefit'][k][l] * islocated[(k, l)]
               for k in range(K) for l in range(L))

problem += total_cost

# Constraints
# Each department can only be located in one city
for k in range(K):
    problem += pulp.lpSum(islocated[(k, l)] for l in range(L)) == 1

# No city can host more than three departments
for l in range(L):
    problem += pulp.lpSum(islocated[(k, l)] for k in range(K)) <= 3

# Solve the problem
problem.solve()

# Output result
islocated_result = [[int(islocated[(k, l)].varValue) for l in range(L)] for k in range(K)]
output = {"islocated": islocated_result}
print(json.dumps(output))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
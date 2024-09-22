import pulp
import json

data = {'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]], 
        'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], 
                         [0.0, 0.0, 1.4, 1.2, 0.0], 
                         [1.0, 1.4, 0.0, 0.0, 2.0], 
                         [1.5, 1.2, 0.0, 2.0, 0.7], 
                         [0.0, 0.0, 2.0, 0.7, 0.0]], 
        'cost': [[5, 14, 13], 
                 [15, 5, 9], 
                 [13, 9, 10]]}

# Parameters
K = len(data['benefit'])  # number of departments
L = len(data['benefit'][0])  # number of cities
benefit = data['benefit']
communication = data['communication']
cost = data['cost']

# Model
problem = pulp.LpProblem("Department_Location", pulp.LpMinimize)

# Decision Variables
islocated = pulp.LpVariable.dicts("islocated", (range(K), range(L)), 
                                    cat='Binary')

# Objective Function
total_cost = pulp.lpSum(
    (pulp.lpSum(communication[k][j] * cost[l][m] * islocated[k][l] for j in range(K) for m in range(L) if j != m) 
     - benefit[k][l] * islocated[k][l]) 
    for k in range(K) for l in range(L)
)

problem += total_cost

# Constraints
# Each department must be located in one city
for k in range(K):
    problem += pulp.lpSum(islocated[k][l] for l in range(L)) == 1

# No city can have more than three departments
for l in range(L):
    problem += pulp.lpSum(islocated[k][l] for k in range(K)) <= 3

# Solve the problem
problem.solve()

# Extracting the results
islocated_result = [[pulp.value(islocated[k][l]) for l in range(L)] for k in range(K)]

# Output result
output = {
    "islocated": islocated_result
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
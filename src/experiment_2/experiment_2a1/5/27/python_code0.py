import pulp
import json

data = {'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]], 
        'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], 
                         [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], 
                         [0.0, 0.0, 2.0, 0.7, 0.0]], 
        'cost': [[5, 14, 13], [15, 5, 9], [13, 9, 10]]}

K = len(data['benefit'])  # Number of departments
L = len(data['benefit'][0])  # Number of locations

# Create the problem
problem = pulp.LpProblem("Department_Location_Problem", pulp.LpMinimize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", 
                                    ((k, l) for k in range(K) for l in range(L)), 
                                    cat='Binary')

# Objective function
total_cost = pulp.lpSum(
    (data['cost'][l][m] * data['communication'][k][m] 
     for k in range(K) for l in range(L) for m in range(K)) 
    - (1 * data['benefit'][k][l] * islocated[(k, l)] 
    for k in range(K) for l in range(L))
)
problem += total_cost

# Constraints
# Each department must be located in exactly one city
for k in range(K):
    problem += pulp.lpSum(islocated[(k, l)] for l in range(L)) == 1

# No city can have more than three departments
for l in range(L):
    problem += pulp.lpSum(islocated[(k, l)] for k in range(K)) <= 3

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "islocated": [[int(islocated[(k, l)].varValue) for l in range(L)] for k in range(K)]
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
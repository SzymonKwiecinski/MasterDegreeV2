import pulp

# Input data
data = {
    "benefit": [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    "communication": [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]],
    "cost": [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}

benefit = data['benefit']
communication = data['communication']
cost = data['cost']

K = len(benefit)  # Number of departments
L = len(benefit[0])  # Number of cities

# Define the problem
problem = pulp.LpProblem("Department_Location", pulp.LpMinimize)

# Decision Variables
islocated = pulp.LpVariable.dicts("islocated", [(k, l) for k in range(K) for l in range(L)], 0, 1, pulp.LpBinary)

# Objective Function
cost_expr = pulp.lpSum(
    -benefit[k][l] * islocated[(k, l)] 
    for k in range(K) 
    for l in range(L)
)

# Communication costs
comm_cost_expr = pulp.lpSum(
    communication[k][j] * cost[l][m] * islocated[(k, l)] * islocated[(j, m)]
    for k in range(K) 
    for j in range(K) 
    for l in range(L) 
    for m in range(L)
)

# Total cost to be minimized
problem += cost_expr + comm_cost_expr

# Constraints
# Each department is assigned to one city
for k in range(K):
    problem += pulp.lpSum(islocated[(k, l)] for l in range(L)) == 1

# No city can have more than three departments
for l in range(L):
    problem += pulp.lpSum(islocated[(k, l)] for k in range(K)) <= 3

# Solve the problem
problem.solve(pulp.PULP_CBC_CMD(msg=0))

# Prepare output
output = {
    "islocated": [[int(islocated[(k, l)].varValue) for l in range(L)] for k in range(K)],
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
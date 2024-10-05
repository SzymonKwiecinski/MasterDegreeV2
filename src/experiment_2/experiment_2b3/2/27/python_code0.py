import pulp

data = {
    "benefit": [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    "communication": [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]], 
    "cost": [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}

benefits = data['benefit']
communication = data['communication']
cost = data['cost']

K = len(benefits)
L = len(benefits[0])

# Define Problem
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision Variables
islocated = pulp.LpVariable.dicts("islocated", ((k, l) for k in range(K) for l in range(L)), cat='Binary')

# Objective Function
total_cost = pulp.lpSum(
    -benefits[k][l] * islocated[k, l] +
    pulp.lpSum(
        communication[k][j] * cost[l][m] * islocated[j, m]
        for j in range(K) for m in range(L)
    )
    for k in range(K) for l in range(L)
)

problem += total_cost

# Constraints

# Each department must be located in exactly one city
for k in range(K):
    problem += pulp.lpSum(islocated[k, l] for l in range(L)) == 1

# No more than 3 departments in any city
for l in range(L):
    problem += pulp.lpSum(islocated[k, l] for k in range(K)) <= 3

# Solve the problem
problem.solve(pulp.PULP_CBC_CMD(msg=False))

# Prepare the output
output = {
    "islocated": [[int(islocated[k, l].varValue) for l in range(L)] for k in range(K)]
}

# Print the results
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
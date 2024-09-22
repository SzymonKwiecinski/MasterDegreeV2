import pulp

# Data
data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    'communication': [
        [0.0, 0.0, 1.0, 1.5, 0.0],
        [0.0, 0.0, 1.4, 1.2, 0.0],
        [1.0, 1.4, 0.0, 0.0, 2.0],
        [1.5, 1.2, 0.0, 2.0, 0.7],
        [0.0, 0.0, 2.0, 0.7, 0.0]
    ],
    'cost': [
        [5, 14, 13],
        [15, 5, 9],
        [13, 9, 10]
    ]
}

benefit = data['benefit']
communication = data['communication']
cost = data['cost']

K = len(benefit)
L = len(benefit[0])
M = len(cost[0])

# Initialize the problem
problem = pulp.LpProblem("FacilityLocation", pulp.LpMinimize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", ((k, l) for k in range(K) for l in range(L)), cat='Binary')

# Objective function
objective = pulp.lpSum(
    -benefit[k][l] * islocated[k, l]
    + sum(
        communication[k][j] * cost[l][m] * islocated[k, l] * islocated[j, m]
        for j in range(K) for m in range(L)
    )
    for k in range(K) for l in range(L)
)

problem += objective

# Constraints
# Each entity is located at exactly one location
for k in range(K):
    problem += pulp.lpSum(islocated[k, l] for l in range(L)) == 1

# No more than 3 entities can be located at each location
for l in range(L):
    problem += pulp.lpSum(islocated[k, l] for k in range(K)) <= 3

# Solve the problem
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
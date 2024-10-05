import pulp

# Problem data
data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]],
    'cost': [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}

benefit = data['benefit']
communication = data['communication']
cost = data['cost']

K = len(communication)  # Number of departments
L = len(cost)  # Number of cities

# Create the problem
problem = pulp.LpProblem("Relocation", pulp.LpMinimize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", ((k, l) for k in range(K) for l in range(L)), cat='Binary')

# Objective function
communication_cost = pulp.lpSum(
    communication[k][j] * cost[l][m] * islocated[k, l] * islocated[j, m]
    for k in range(K) for j in range(K) for l in range(L) for m in range(L)
)
benefit_gain = pulp.lpSum(
    benefit[k][l] * islocated[k, l]
    for k in range(K) for l in range(L)
)
total_cost = communication_cost - benefit_gain
problem += total_cost

# Constraints

# Each department must be relocated to exactly one city
for k in range(K):
    problem += pulp.lpSum(islocated[k, l] for l in range(L)) == 1

# No city may have more than 3 departments
for l in range(L):
    problem += pulp.lpSum(islocated[k, l] for k in range(K)) <= 3

# Solve the problem
problem.solve()

# Gather results
result_islocated = [[pulp.value(islocated[k, l]) for l in range(L)] for k in range(K)]

print({
    "islocated": result_islocated,
})

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
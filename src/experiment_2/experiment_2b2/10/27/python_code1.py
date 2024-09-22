import pulp

# Data from JSON
data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]],
    'cost': [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}

# Extracting data
K = len(data['benefit'])
L = len(data['benefit'][0])
benefit = data['benefit']
communication = data['communication']
cost = data['cost']

# Define problem
problem = pulp.LpProblem("Relocation_Problem", pulp.LpMinimize)

# Decision variables
islocated = [
    [pulp.LpVariable(f'islocated_{k}_{l}', cat='Binary') for l in range(L)]
    for k in range(K)
]

# Objective: Minimize total cost
total_benefit = pulp.lpSum(
    islocated[k][l] * benefit[k][l] for k in range(K) for l in range(L)
)

# Correctly calculate communication costs
total_communication_cost = pulp.lpSum(
    communication[k][j] * cost[l][m] * islocated[k][l] * islocated[j][m]
    for k in range(K) for j in range(K) for l in range(L) for m in range(L)
    if k != j and l != m  # exclude self-communication
)

problem += (- total_benefit + total_communication_cost), "Total_Cost"

# Constraints

# Each department should be located in exactly one city
for k in range(K):
    problem += pulp.lpSum(islocated[k][l] for l in range(L)) == 1, f"Dept_Location_{k}"

# No city can have more than three departments
for l in range(L):
    problem += pulp.lpSum(islocated[k][l] for k in range(K)) <= 3, f"City_Capacity_{l}"

# Solve the problem
problem.solve()

# Output result
result = {
    "islocated": [
        [pulp.value(islocated[k][l]) for l in range(L)]
        for k in range(K)
    ]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
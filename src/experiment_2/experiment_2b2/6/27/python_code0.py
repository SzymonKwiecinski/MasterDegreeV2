import pulp

# Input Data
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

# Indices
K = len(benefit)      # Number of departments
L = len(benefit[0])   # Number of cities

# Create the LP problem
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision Variables
islocated = pulp.LpVariable.dicts(
    "islocated",
    ((k, l) for k in range(K) for l in range(L)),
    cat=pulp.LpBinary
)

# Objective Function: Minimize total cost including benefits and communication costs
obj = pulp.lpSum(
    (islocated[(k, l)] * benefit[k][l] * -1) +
    pulp.lpSum(
        islocated[(k, l)] * islocated[(j, m)] * communication[k][j] * cost[l][m]
        for j in range(K) for m in range(L)
    )
    for k in range(K) for l in range(L)
)

problem += obj

# Constraints
# Each department must be located in exactly one city
for k in range(K):
    problem += pulp.lpSum(islocated[(k, l)] for l in range(L)) == 1

# No more than three departments can be located in a single city
for l in range(L):
    problem += pulp.lpSum(islocated[(k, l)] for k in range(K)) <= 3

# Solve the problem
problem.solve()

# Extract results
islocated_result = [
    [int(pulp.value(islocated[(k, l)])) for l in range(L)]
    for k in range(K)
]

# Print output
output = {
    "islocated": islocated_result
}
print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp

# Data from the input
benefit = [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]]
communication = [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]]
cost = [[5, 14, 13], [15, 5, 9], [13, 9, 10]]

# Problem dimensions
K = len(benefit)  # number of departments
L = len(benefit[0])  # number of cities

# Define the problem
problem = pulp.LpProblem("Department_Relocation_Problem", pulp.LpMinimize)

# Decision variables
islocated = [[pulp.LpVariable(f"islocated_{k}_{l}", cat='Binary') for l in range(L)] for k in range(K)]

# Objective function components

# Linear benefits
benefit_cost = pulp.lpSum([
    islocated[k][l] * -benefit[k][l]
    for k in range(K) for l in range(L)
])

# Linear Communication costs
communication_cost = pulp.lpSum(
    communication[k][j] * cost[l][m] * islocated[k][l] * islocated[j][m]
    for k in range(K) for j in range(K) 
    for l in range(L) for m in range(L)
)

# Objective function
problem += benefit_cost + communication_cost

# Constraints

# Each department must be in exactly one location
for k in range(K):
    problem += pulp.lpSum(islocated[k][l] for l in range(L)) == 1

# No city can host more than 3 departments
for l in range(L):
    problem += pulp.lpSum(islocated[k][l] for k in range(K)) <= 3

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "islocated": [[int(islocated[k][l].varValue) for l in range(L)] for k in range(K)]
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
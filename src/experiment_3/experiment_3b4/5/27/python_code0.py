import pulp

# Data
benefit = [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]]
communication = [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]]
cost = [[5, 14, 13], [15, 5, 9], [13, 9, 10]]

K = len(benefit)  # Number of departments
L = len(benefit[0])  # Number of cities

# Problem
problem = pulp.LpProblem("Department_City_Assignment", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", ((k, l) for k in range(K) for l in range(L)), cat='Binary')

# Objective Function
objective = pulp.lpSum([-benefit[k][l] * x[k, l] for k in range(K) for l in range(L)]) + \
            pulp.lpSum([communication[k][j] * cost[l][m] * x[k, l] * x[j, m]
                        for k in range(K) for l in range(L)
                        for j in range(K) for m in range(L)])

problem += objective

# Constraints
# Each department must be located in exactly one city
for k in range(K):
    problem += pulp.lpSum([x[k, l] for l in range(L)]) == 1

# No city can have more than three departments
for l in range(L):
    problem += pulp.lpSum([x[k, l] for k in range(K)]) <= 3

# Solve the problem
problem.solve()

# Print the results
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
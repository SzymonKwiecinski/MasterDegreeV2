import pulp
import json

# Data
data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]],
    'cost': [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}

# Model
K = len(data['benefit'])  # Number of departments
L = len(data['benefit'][0])  # Number of cities
problem = pulp.LpProblem("Department_Relocation", pulp.LpMinimize)

# Decision Variables
x = pulp.LpVariable.dicts("x", (range(K), range(L)), cat='Binary')

# Objective Function
objective = pulp.lpSum(
    -data['benefit'][k][l] * x[k][l] for k in range(K) for l in range(L)
) + pulp.lpSum(
    data['communication'][k][j] * data['cost'][l][m] * x[k][l] * x[j][m]
    for k in range(K) for j in range(K) for l in range(L) for m in range(L)
)

problem += objective

# Constraints
# Each department is located in one city
for k in range(K):
    problem += pulp.lpSum(x[k][l] for l in range(L)) == 1

# No more than three departments can be located in the same city
for l in range(L):
    problem += pulp.lpSum(x[k][l] for k in range(K)) <= 3

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
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

K = len(benefit)  # Number of departments
L = len(benefit[0])  # Number of cities

# Problem
problem = pulp.LpProblem("Department_Location_Minimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((k, l) for k in range(K) for l in range(L)), cat='Binary')

# Objective function
problem += (
    pulp.lpSum(x[k, l] * benefit[k][l] for k in range(K) for l in range(L)) +
    pulp.lpSum(x[k, l] * x[j, m] * communication[k][j] * cost[l][m] 
               for k in range(K) for j in range(K) for l in range(L) for m in range(L))
)

# Constraints

# Each department is located in exactly one city
for k in range(K):
    problem += pulp.lpSum(x[k, l] for l in range(L)) == 1, f"Dept_{k}_one_city"

# No city hosts more than three departments
for l in range(L):
    problem += pulp.lpSum(x[k, l] for k in range(K)) <= 3, f"City_{l}_at_most_3_depts"

# Solve
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
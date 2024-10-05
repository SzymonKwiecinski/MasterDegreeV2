import pulp

# Data provided
data = {
    'benefit': [[10, 10], [15, 20], [10, 15], [20, 15], [5, 15]],
    'communication': [[0.0, 0.0, 1.0, 1.5, 0.0], [0.0, 0.0, 1.4, 1.2, 0.0], [1.0, 1.4, 0.0, 0.0, 2.0], [1.5, 1.2, 0.0, 2.0, 0.7], [0.0, 0.0, 2.0, 0.7, 0.0]],
    'cost': [[5, 14, 13], [15, 5, 9], [13, 9, 10]]
}

# Sets
K = len(data['benefit'])  # Number of departments
L = len(data['benefit'][0])  # Number of cities

# Problem setup
problem = pulp.LpProblem("DepartmentRelocation", pulp.LpMinimize)

# Decision variables
islocated = pulp.LpVariable.dicts("islocated", ((k, l) for k in range(K) for l in range(L)), cat='Binary')

# Objective Function
communication_cost = sum(
    sum(
        data['communication'][k][j] * sum(data['cost'][l]) * islocated[(k, l)]
        for j in range(K) if k != j
    )
    for k in range(K) for l in range(L)
)

benefit_gain = sum(
    data['benefit'][k][l] * islocated[(k, l)]
    for k in range(K) for l in range(L)
)

problem += communication_cost - benefit_gain

# Constraints

# Each department can be located in only one city
for k in range(K):
    problem += sum(islocated[(k, l)] for l in range(L)) <= 1

# No city can host more than three departments
for l in range(L):
    problem += sum(islocated[(k, l)] for k in range(K)) <= 3

# Solving the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Additionally, print which departments are located in which cities
for k in range(K):
    for l in range(L):
        if pulp.value(islocated[(k, l)]) == 1:
            print(f'Department {k+1} is located in City {l+1}')
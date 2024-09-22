import pulp

# Data from the problem
data = {
    'numdepot': [3, 3, 4],
    'numport': [1, 6, 3],
    'price': 3.0,
    'distance': [[0.0, 2.0, 5.0], [2.0, 0.0, 3.0], [5.0, 3.0, 0.0]]
}

# Indices
I = len(data['numdepot'])
J = len(data['numport'])

# Problem
problem = pulp.LpProblem("SupplyChainOptimization", pulp.LpMinimize)

# Decision variables
x = pulp.LpVariable.dicts("x", ((i, j) for i in range(I) for j in range(J)), lowBound=0, cat=pulp.LpInteger)

# Objective function
objective = pulp.lpSum((x[i, j] / 2) * data['price'] * data['distance'][i][j] for i in range(I) for j in range(J))
problem += objective

# Constraints
# Depot capacity constraint
for i in range(I):
    problem += pulp.lpSum(x[i, j] for j in range(J)) <= data['numdepot'][i]

# Port demand constraint
for j in range(J):
    problem += pulp.lpSum(x[i, j] for i in range(I)) >= data['numport'][j]

# Solve the problem
problem.solve()

# Print the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
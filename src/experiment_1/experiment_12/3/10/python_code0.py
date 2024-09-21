import pulp

# Data from JSON
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Number of foods and nutrients
K = len(data['price'])
M = len(data['demand'])

# Problem
problem = pulp.LpProblem("Food_Selection", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(data['price'][k] * x[k] for k in range(K))

# Constraints
for m in range(M):
    problem += (pulp.lpSum(data['nutrition'][k][m] * x[k] for k in range(K)) >= data['demand'][m], f'Nutrient_{m}_Demand')

# Solve the problem
problem.solve()

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
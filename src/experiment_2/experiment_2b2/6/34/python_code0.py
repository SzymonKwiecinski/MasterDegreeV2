import pulp

# Data input
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Create problem
problem = pulp.LpProblem("Minimize_Food_Cost", pulp.LpMinimize)

# Number of foods and nutrients
K = len(data['price'])
M = len(data['demand'])

# Variables: quantity of each food to purchase
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Minimize total cost
problem += pulp.lpSum(data['price'][k] * quantity[k] for k in range(K))

# Constraints: Nutrition requirements for each nutrient
for m in range(M):
    problem += pulp.lpSum(data['nutrition'][k][m] * quantity[k] for k in range(K)) >= data['demand'][m]

# Solve the problem
problem.solve()

# Results
output = {"quantity": [pulp.value(quantity[k]) for k in range(K)]}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
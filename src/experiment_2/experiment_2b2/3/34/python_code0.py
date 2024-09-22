import pulp

# Data
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

price = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Number of foods and nutrients
K = len(price)
M = len(demand)

# Problem
problem = pulp.LpProblem("BalancedDietProblem", pulp.LpMinimize)

# Variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective
problem += pulp.lpSum(price[k] * quantity[k] for k in range(K)), "Total Cost"

# Constraints
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantity[k] for k in range(K)) >= demand[m], f'Nutrient_{m}_Demand'

# Solve
problem.solve()

# Output
output = {
    "quantity": [pulp.value(quantity[k]) for k in range(K)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
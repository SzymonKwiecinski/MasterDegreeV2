import pulp

# Data
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [
        [3, 5],
        [1, 3],
        [4, 4]
    ]
}

# Extract data
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Number of different foods and nutrients
K = len(price)
M = len(demand)

# Problem
problem = pulp.LpProblem("Nutritional_Food_Purchase", pulp.LpMinimize)

# Decision Variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum([price[k] * quantity[k] for k in range(K)])

# Constraints
for m in range(M):
    problem += pulp.lpSum([nutrition[k][m] * quantity[k] for k in range(K)]) >= demand[m]

# Solve
problem.solve()

# Objective Value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
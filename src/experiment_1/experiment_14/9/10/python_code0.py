import pulp

# Data
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Parameters
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

K = len(price)  # Number of different types of food
M = len(demand)  # Number of nutrients to consider

# Problem
problem = pulp.LpProblem("Food Selection Problem", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum([price[k] * x[k] for k in range(K)])

# Constraints
# Demand satisfaction for each nutrient
for m in range(M):
    problem += pulp.lpSum([nutrition[k][m] * x[k] for k in range(K)]) >= demand[m]

# Solve the problem
problem.solve()

# Print the results
for k in range(K):
    print(f'x_{k} = {pulp.value(x[k])}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
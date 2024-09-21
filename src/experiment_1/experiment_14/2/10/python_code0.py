import pulp

# Data from the JSON input
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Extracting data
prices = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Number of food types and nutrients
K = len(prices)
M = len(demand)

# Create the problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K))

# Constraints
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * x[k] for k in range(K)) >= demand[m]

# Solve the problem
problem.solve()

# Output the results
print(f'Status: {pulp.LpStatus[problem.status]}')
for k in range(K):
    print(f'Food {k+1}: {x[k].varValue}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp

# Parse the data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Extract information from data
prices = data['price']
demands = data['demand']
nutrition = data['nutrition']

# Number of foods and nutrients
K = len(prices)
M = len(demands)

# Create the problem
problem = pulp.LpProblem("Nutrient_Minimization", pulp.LpMinimize)

# Decision variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function
problem += pulp.lpSum(prices[k] * x[k] for k in range(K))

# Constraints
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * x[k] for k in range(K)) >= demands[m]

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
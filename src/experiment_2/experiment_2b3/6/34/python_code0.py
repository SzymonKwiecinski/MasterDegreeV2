import pulp

# Load the data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}

# Set up basic parameters
prices = data['price']
demands = data['demand']
nutritions = data['nutrition']

# Number of foods and nutrients
K = len(prices)
M = len(demands)

# Create the LP problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision variables: quantity of each food to purchase
quantities = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: minimize total cost
problem += pulp.lpSum(prices[k] * quantities[k] for k in range(K))

# Constraints: Meet the nutritional demands
for m in range(M):
    problem += pulp.lpSum(nutritions[k][m] * quantities[k] for k in range(K)) >= demands[m]

# Solve the problem
problem.solve()

# Get the results
solution = {'quantity': [quantities[k].varValue for k in range(K)]}

# Print the solution
print(solution)

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
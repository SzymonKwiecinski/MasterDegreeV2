import pulp

# Data provided
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Extracting data for ease of use
prices = data['price']
demands = data['demand']
nutrition = data['nutrition']

# Number of food types (K) and nutrients (M)
K = len(prices)
M = len(demands)

# Initialize the problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Decision variables: x_k >= 0 for each food type k
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective function: Minimize the total cost
problem += pulp.lpSum(prices[k] * x[k] for k in range(K)), "Total Cost"

# Constraints: Each nutrient demand must be met
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * x[k] for k in range(K)) >= demands[m], f"Demand_Constraint_{m}"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp

# Extracted data from JSON
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Parameters
prices = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Number of foods (K) and nutrients (M)
K = len(prices)
M = len(demand)

# Problem definition
problem = pulp.LpProblem("Nutritional_Optimization", pulp.LpMinimize)

# Decision Variables
quantities = [pulp.LpVariable(f"quantity_{k}", lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum([prices[k] * quantities[k] for k in range(K)])

# Constraints
for m in range(M):
    problem += pulp.lpSum([nutrition[k][m] * quantities[k] for k in range(K)]) >= demand[m]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
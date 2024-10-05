import pulp

# Data
data = {'price': [1, 2, 3], 'demand': [10, 20], 'nutrition': [[3, 5], [1, 3], [4, 4]]}
price = data['price']
demand = data['demand']
nutrition = data['nutrition']
K = len(price)  # Number of food items
M = len(demand)  # Number of nutrients

# Create the LP problem
problem = pulp.LpProblem("Minimize_Food_Cost", pulp.LpMinimize)

# Decision variables
quantity = pulp.LpVariable.dicts("quantity", range(K), lowBound=0)

# Objective Function
problem += pulp.lpSum(price[k] * quantity[k] for k in range(K)), "Total_Cost"

# Constraints
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantity[k] for k in range(K)) >= demand[m], f"Demand_Constraint_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
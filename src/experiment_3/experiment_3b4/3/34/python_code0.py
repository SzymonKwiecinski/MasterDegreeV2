import pulp

# Data from JSON
price = [1, 2, 3]
demand = [10, 20]
nutrition = [
    [3, 5],  # nutrient units per unit of food 1
    [1, 3],  # nutrient units per unit of food 2
    [4, 4]   # nutrient units per unit of food 3
]

# Number of foods and nutrients
K = len(price)
M = len(demand)

# Defining the Linear Programming problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision Variables
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum(price[k] * quantity[k] for k in range(K)), "Total Cost"

# Constraints
for m in range(M):
    problem += pulp.lpSum(nutrition[k][m] * quantity[k] for k in range(K)) >= demand[m], f"Nutrient_{m}_Requirement"

# Solve the problem
problem.solve()

# Output the results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
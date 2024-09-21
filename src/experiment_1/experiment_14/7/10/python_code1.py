import pulp

# Data from the JSON
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Parameters
K = len(data['price'])  # Number of food types
M = len(data['demand'])  # Number of nutrients

Price = data['price']
Demand = data['demand']
Nutrition = data['nutrition']

# Problem
problem = pulp.LpProblem("Food_Selection_Problem", pulp.LpMinimize)

# Decision Variables
x = [pulp.LpVariable(f'x_{k}', lowBound=0, cat='Continuous') for k in range(K)]

# Objective Function
problem += pulp.lpSum(Price[k] * x[k] for k in range(K)), "Total_Cost"

# Constraints
# Nutrient demand constraints
for m in range(M):
    problem += pulp.lpSum(Nutrition[k][m] * x[k] for k in range(K)) >= Demand[m], f"Nutrient_{m}_Demand"

# Solve the problem
problem.solve()

# Print the results
for k in range(K):
    print(f'Units of food {k+1} to purchase: {x[k].varValue}')

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
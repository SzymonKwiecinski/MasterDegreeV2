import pulp

# Input data
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

# Extract data
price = data['price']
demand = data['demand']
nutrition = data['nutrition']

# Problem
problem = pulp.LpProblem("Nutritional_Diet_Problem", pulp.LpMinimize)

# Variables: quantity of each food to purchase
quantity = [pulp.LpVariable(f'quantity_{k}', lowBound=0, cat='Continuous') for k in range(len(price))]

# Objective function: Minimize the total price
problem += pulp.lpSum([price[k] * quantity[k] for k in range(len(price))]), "Total_Cost"

# Constraints: Nutritional demands
for m in range(len(demand)):
    problem += (pulp.lpSum([nutrition[k][m] * quantity[k] for k in range(len(price))]) >= demand[m],
                f'Nutrient_Requirement_{m}')

# Solve the problem
problem.solve()

# Output the solution
solution = {
    'quantity': [pulp.value(quantity[k]) for k in range(len(quantity))]
}

print(solution)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
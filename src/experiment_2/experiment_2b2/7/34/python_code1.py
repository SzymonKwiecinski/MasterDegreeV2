from pulp import LpProblem, LpMinimize, LpVariable, lpSum, value

# Data Input
data = {
    'price': [1, 2, 3],
    'demand': [10, 20],
    'nutrition': [[3, 5], [1, 3], [4, 4]]
}

prices = data['price']
demands = data['demand']
nutritions = data['nutrition']

# Problem Initialization
problem = LpProblem("Balanced_Diet_Problem", LpMinimize)

# Decision Variables: Quantity of food to purchase
num_foods = len(prices)
quantity_vars = [LpVariable(f'quantity_{k}', lowBound=0) for k in range(num_foods)]

# Objective Function: Minimize total cost
problem += lpSum(prices[k] * quantity_vars[k] for k in range(num_foods))

# Constraints: Satisfy nutritional demands
num_nutrients = len(demands)
for m in range(num_nutrients):
    problem += lpSum(nutritions[k][m] * quantity_vars[k] for k in range(num_foods)) >= demands[m]

# Solve the problem
problem.solve()

# Prepare the result
result = {
    "quantity": [quantity_vars[k].varValue for k in range(num_foods)]
}

print(result)
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')
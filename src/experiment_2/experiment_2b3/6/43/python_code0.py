import pulp

# Problem Data
data = {
    'available': [240000, 8000, 75000],
    'requirements': [[48, 1, 10], [40, 1, 10], [0, 1, 2]],
    'prices': [40, 38, 9],
    'costs': [30, 26, 7],
    'demands': [10000, 2000, 10000]
}

# Extract data from input
available = data['available']
requirements = data['requirements']
prices = data['prices']
costs = data['costs']
demands = data['demands']

# Number of materials and products
num_materials = len(available)
num_products = len(prices)

# Define problem
problem = pulp.LpProblem("Maximize Profit", pulp.LpMaximize)

# Decision variables: amount to produce of each product
amount_vars = [pulp.LpVariable(f'amount_{j}', lowBound=0, cat='Continuous') for j in range(num_products)]

# Objective function: Maximize total profit
profit = pulp.lpSum((prices[j] - costs[j]) * amount_vars[j] for j in range(num_products))
problem += profit

# Constraints for raw material availability
for i in range(num_materials):
    material_constraint = pulp.lpSum(requirements[j][i] * amount_vars[j] for j in range(num_products))
    problem += material_constraint <= available[i]

# Constraints for maximum demand
for j in range(num_products):
    problem += amount_vars[j] <= demands[j]

# Solve problem
problem.solve()

# Output
amount = [pulp.value(amount_vars[j]) for j in range(num_products)]
total_profit = pulp.value(problem.objective)

output = {
    "amount": amount,
    "total_profit": total_profit
}

print(output)
print(f' (Objective Value): <OBJ>{total_profit}</OBJ>')
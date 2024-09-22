import pulp

# Data
data = {
    'alloy_quant': 1000,
    'target': [300, 700],
    'ratio': [
        [0.1, 0.9],
        [0.25, 0.75],
        [0.5, 0.5],
        [0.75, 0.25],
        [0.95, 0.05]
    ],
    'price': [5, 4, 3, 2, 1.5]
}

# Parameters
alloy_quant = data['alloy_quant']
target = data['target']
ratios = data['ratio']
prices = data['price']

# Number of alloys and metals
num_alloys = len(prices)
num_metals = len(target)

# Problem
problem = pulp.LpProblem("Alloy_Production", pulp.LpMinimize)

# Variables: amount of each alloy to be purchased
amount = [pulp.LpVariable(f'amount_{k}', lowBound=0) for k in range(num_alloys)]

# Objective function: Minimize the total cost
problem += pulp.lpSum(prices[k] * amount[k] for k in range(num_alloys))

# Constraint 1: Total weight of the alloys must equal the desired alloy weight
problem += pulp.lpSum(amount) == alloy_quant

# Constraint 2: Each metal must meet its target requirement
for m in range(num_metals):
    problem += pulp.lpSum(ratios[k][m] * amount[k] for k in range(num_alloys)) == target[m]

# Solve the problem
problem.solve()

# Output the quantities of each alloy to be purchased
amount_values = [pulp.value(amount[k]) for k in range(num_alloys)]
print(f'Quantities to purchase: {amount_values}')

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
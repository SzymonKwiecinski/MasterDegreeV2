import pulp
import json

# Data from JSON
data = {
    'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], 
                  [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
    'sell_price': 150,
    'is_vegetable': [True, True, False, False, False],
    'max_vegetable_refining_per_month': 200,
    'max_non_vegetable_refining_per_month': 250,
    'storage_size': 1000,
    'storage_cost': 5,
    'min_hardness': 3,
    'max_hardness': 6,
    'hardness': [8.8, 6.1, 2.0, 4.2, 5.0],
    'init_amount': 500,
    'min_usage': 20,
    'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
}

# Parameters
months = len(data['buy_price'])
oils = len(data['buy_price'][0])
sell_price = data['sell_price']
storage_cost = data['storage_cost']
max_hardness = data['max_hardness']
min_hardness = data['min_hardness']
init_amount = data['init_amount']
min_usage = data['min_usage']
max_veg = data['max_vegetable_refining_per_month']
max_non_veg = data['max_non_vegetable_refining_per_month']
dependencies = data['dependencies']

# Setup the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buy", ((i, m) for i in range(oils) for m in range(months)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(oils) for m in range(months)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(oils) for m in range(months)), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum((sell_price * pulp.lpSum(refine[i, m] for i in range(oils) for m in range(months))) 
                     - pulp.lpSum(data['buy_price'][m][i] * buyquantity[i, m] for i in range(oils) for m in range(months))
                     - pulp.lpSum(storage_cost * storage[i, m] for i in range(oils) for m in range(months)))
problem += profit

# Constraints
for m in range(months):
    for i in range(oils):
        # Storage and buy quantities
        if m == 0:
            problem += storage[i, m] == init_amount + buyquantity[i, m] - refine[i, m]
        else:
            problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m] - refine[i, m]
        
        problem += storage[i, m] <= data['storage_size']  # Max storage constraint

        # Dependency constraints
        if data['dependencies'][i][-1] == 1:  # If oil i requires oil 4
            problem += (refine[i, m] <= pulp.lpSum(refine[j, m] for j in range(oils) if j != i))  # requirement for oil 4

    # Refining amount constraints
    problem += pulp.lpSum(refine[i, m] for i in range(oils) if data['is_vegetable'][i]) <= max_veg
    problem += pulp.lpSum(refine[i, m] for i in range(oils) if not data['is_vegetable'][i]) <= max_non_veg

# Hardness constraints
for m in range(months):
    problem += (pulp.lpSum(refine[i, m] * data['hardness'][i] for i in range(oils)) / 
                 pulp.lpSum(refine[i, m] for i in range(oils) if refine[i, m] > 0) >= min_hardness)
    problem += (pulp.lpSum(refine[i, m] * data['hardness'][i] for i in range(oils)) / 
                 pulp.lpSum(refine[i, m] for i in range(oils) if refine[i, m] > 0) <= max_hardness)

# The last month storage constraint
for i in range(oils):
    problem += storage[i, months-1] == init_amount

# Solve the problem
problem.solve()

# Prepare solution data
solution = {
    "buy": [[pulp.value(buyquantity[i, m]) for i in range(oils)] for m in range(months)],
    "refine": [[pulp.value(refine[i, m]) for i in range(oils)] for m in range(months)],
    "storage": [[pulp.value(storage[i, m]) for i in range(oils)] for m in range(months)]
}

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Return the solution
solution
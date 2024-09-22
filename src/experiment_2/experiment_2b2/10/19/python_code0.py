import pulp

# Data from JSON
data = {
    'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
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

# Constants
months = len(data['buy_price'])
oils = len(data['buy_price'][0])
sell_price = data['sell_price']
max_veg = data['max_vegetable_refining_per_month']
max_non_veg = data['max_non_vegetable_refining_per_month']
storage_size = data['storage_size']
storage_cost = data['storage_cost']
max_hardness = data['max_hardness']
min_hardness = data['min_hardness']
init_amount = data['init_amount']
min_usage = data['min_usage']
is_vegetable = data['is_vegetable']
hardness = data['hardness']
dependencies = data['dependencies']

# Define the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
buy = pulp.LpVariable.dicts("Buy", ((i, m) for i in range(oils) for m in range(months)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(oils) for m in range(months)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(oils) for m in range(months + 1)), lowBound=0, cat='Continuous')
usage_binary = pulp.LpVariable.dicts("UsageBinary", ((i, m) for i in range(oils) for m in range(months)), cat='Binary')

# Objective function
revenue = pulp.lpSum((sell_price * pulp.lpSum(refine[i, m] for i in range(oils)) - 
                      pulp.lpSum(data['buy_price'][m][i] * buy[i, m] for i in range(oils)) - 
                      storage_cost * pulp.lpSum(storage[i, m] for i in range(oils)))
                     for m in range(months))
problem += revenue

# Constraints
for m in range(months):
    # Balance equation and storage constraints
    for i in range(oils):
        problem += storage[i, m + 1] == storage[i, m] + buy[i, m] - refine[i, m]
        problem += storage[i, m] <= storage_size

    # Refining constraints
    veg_refine = pulp.lpSum(refine[i, m] for i in range(oils) if is_vegetable[i])
    non_veg_refine = pulp.lpSum(refine[i, m] for i in range(oils) if not is_vegetable[i])
    problem += veg_refine <= max_veg
    problem += non_veg_refine <= max_non_veg

    # Hardness constraint
    hardness_constraint = pulp.lpSum(refine[i, m] * hardness[i] for i in range(oils))
    refine_total = pulp.lpSum(refine[i, m] for i in range(oils))
    problem += hardness_constraint <= max_hardness * refine_total
    problem += hardness_constraint >= min_hardness * refine_total

    # Oil usage constraint
    problem += pulp.lpSum(usage_binary[i, m] for i in range(oils)) <= 3
    for i in range(oils):
        problem += refine[i, m] >= min_usage * usage_binary[i, m]
        for j in range(oils):
            if dependencies[i][j] == 1:
                problem += usage_binary[i, m] <= usage_binary[j, m]

# Initial and final storage constraint
for i in range(oils):
    problem += storage[i, 0] == init_amount
    problem += storage[i, months] == init_amount

# Solve the problem
problem.solve()

# Prepare the output
result = {
    "buy": [[buy[i, m].varValue for i in range(oils)] for m in range(months)],
    "refine": [[refine[i, m].varValue for i in range(oils)] for m in range(months)],
    "storage": [[storage[i, m].varValue for i in range(oils)] for m in range(months + 1)]  # Including month 0
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
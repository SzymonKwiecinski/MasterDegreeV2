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

# Extract data
prices = data['buy_price']
sell_price = data['sell_price']
is_vegetable = data['is_vegetable']
max_veg = data['max_vegetable_refining_per_month']
max_non_veg = data['max_non_vegetable_refining_per_month']
storage_size = data['storage_size']
storage_cost = data['storage_cost']
min_hardness = data['min_hardness']
max_hardness = data['max_hardness']
hardness = data['hardness']
init_amount = data['init_amount']
min_usage = data['min_usage']
dependencies = data['dependencies']

# Constants
num_months = len(prices)
num_oils = len(prices[0])

# Decision variables
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

buy = pulp.LpVariable.dicts("Buy", ((m, i) for m in range(num_months) for i in range(num_oils)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", ((m, i) for m in range(num_months) for i in range(num_oils)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((m, i) for m in range(num_months + 1) for i in range(num_oils)), lowBound=0, cat='Continuous')
use_flag = pulp.LpVariable.dicts("UseFlag", ((m, i) for m in range(num_months) for i in range(num_oils)), cat='Binary')

# Initialize initial amount
for i in range(num_oils):
    problem += storage[(0, i)] == init_amount

# Objective function: Maximize profit
problem += pulp.lpSum(
    sell_price * pulp.lpSum(refine[(m, i)] for i in range(num_oils)) -
    pulp.lpSum(buy[(m, i)] * prices[m][i] for i in range(num_oils)) -
    storage_cost * pulp.lpSum(storage[(m + 1, i)] for i in range(num_oils))
    for m in range(num_months)
)

# Constraints
for m in range(num_months):
    vegetable_refine = pulp.lpSum(refine[(m, i)] for i in range(num_oils) if is_vegetable[i])
    non_vegetable_refine = pulp.lpSum(refine[(m, i)] for i in range(num_oils) if not is_vegetable[i])
    
    problem += vegetable_refine <= max_veg
    problem += non_vegetable_refine <= max_non_veg
    
    problem += pulp.lpSum(refine[(m, i)] for i in range(num_oils)) \
               * pulp.lpSum(hardness[i] * refine[(m, i)] for i in range(num_oils)) >= min_hardness * pulp.lpSum(refine[(m, i)] for i in range(num_oils))
    problem += pulp.lpSum(refine[(m, i)] for i in range(num_oils)) \
               * pulp.lpSum(hardness[i] * refine[(m, i)] for i in range(num_oils)) <= max_hardness * pulp.lpSum(refine[(m, i)] for i in range(num_oils))
    
    for i in range(num_oils):
        problem += storage[(m + 1, i)] == storage[(m, i)] + buy[(m, i)] - refine[(m, i)]
        problem += storage[(m + 1, i)] <= storage_size
        problem += refine[(m, i)] >= min_usage * use_flag[(m, i)]
        
        for j in range(num_oils):
            if dependencies[i][j]:
                problem += use_flag[(m, i)] <= use_flag[(m, j)]
                
    problem += pulp.lpSum(use_flag[(m, i)] for i in range(num_oils)) <= 3

for i in range(num_oils):
    problem += storage[(num_months, i)] == init_amount

# Solve the problem
problem.solve()

# Results
result = {
    "buy": [[pulp.value(buy[(m, i)]) for i in range(num_oils)] for m in range(num_months)],
    "refine": [[pulp.value(refine[(m, i)]) for i in range(num_oils)] for m in range(num_months)],
    "storage": [[pulp.value(storage[(m, i)]) for i in range(num_oils)] for m in range(num_months + 1)]
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp

# Load data
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

# Extracting the given parameters
buy_price = data['buy_price']
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
M = len(buy_price)  # Number of months
I = len(buy_price[0])  # Number of oils

# Initialize the problem
problem = pulp.LpProblem("Maximize Profit", pulp.LpMaximize)

# Decision variables
buy = pulp.LpVariable.dicts("buy", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", ((m, i) for m in range(M) for i in range(I)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((m, i) for m in range(M+1) for i in range(I)), lowBound=0, cat='Continuous')
use = pulp.LpVariable.dicts("use", ((m, i) for m in range(M) for i in range(I)), cat='Binary')

# Objective function: maximize profit
profit = pulp.lpSum([(sell_price - buy_price[m][i] - storage_cost) * refine[m, i] for m in range(M) for i in range(I)]) - pulp.lpSum([storage_cost * storage[m, i] for m in range(1, M+1) for i in range(I)])
problem += profit

# Constraints
for m in range(M):
    problem += pulp.lpSum([refine[m, i] for i in range(I) if is_vegetable[i]]) <= max_veg, f'Month_{m}_Veg_Refine_Limit'
    problem += pulp.lpSum([refine[m, i] for i in range(I) if not is_vegetable[i]]) <= max_non_veg, f'Month_{m}_Non_Veg_Refine_Limit'
    problem += pulp.lpSum([use[m, i] for i in range(I)]) <= 3, f'Month_{m}_Max_3_Oils'

    for i in range(I):
        if m == 0:
            problem += storage[0, i] == init_amount
        problem += buy[m, i] + storage[m, i] == refine[m, i] + storage[m+1, i]
        problem += storage[m+1, i] <= storage_size
        problem += refine[m, i] >= min_usage * use[m, i]
        for j in range(I):
            if dependencies[i][j] == 1:
                problem += use[m, i] <= use[m, j], f'Dependency_{i}_{j}_Month_{m}'

    # Hardness constraint
    problem += pulp.lpSum([hardness[i] * (refine[m, i] + storage[m+1, i]) for i in range(I)]) >= min_hardness * pulp.lpSum([refine[m, i] + storage[m+1, i] for i in range(I)])
    problem += pulp.lpSum([hardness[i] * (refine[m, i] + storage[m+1, i]) for i in range(I)]) <= max_hardness * pulp.lpSum([refine[m, i] + storage[m+1, i] for i in range(I)])

# Ensuring storage at end is equal to initial amount
for i in range(I):
    problem += storage[M, i] == init_amount

# Solve the problem
problem.solve()

# Extract results
output = {
    "buy": [[pulp.value(buy[m, i]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[m, i]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[m, i]) for i in range(I)] for m in range(M+1)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
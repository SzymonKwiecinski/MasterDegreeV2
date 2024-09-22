import pulp

# Data Definition
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
OILS = len(data['buy_price'])
MONTHS = len(data['buy_price'][0])

# Define the problem
problem = pulp.LpProblem("Oil_Refinery_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(OILS) for m in range(MONTHS)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(OILS) for m in range(MONTHS)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(OILS) for m in range(MONTHS + 1)), lowBound=0, cat='Continuous')
use = pulp.LpVariable.dicts("use", ((i, m) for i in range(OILS) for m in range(MONTHS)), cat='Binary')
dependent_use = pulp.LpVariable.dicts("dependent_use", ((j, m) for j in range(OILS) for m in range(MONTHS)), cat='Binary')

# Objective Function
profit = pulp.lpSum([data['sell_price'] * refine[i, m] for i in range(OILS) for m in range(MONTHS)]) - \
    pulp.lpSum([data['buy_price'][i][m] * buyquantity[i, m] for i in range(OILS) for m in range(MONTHS)]) - \
    pulp.lpSum([data['storage_cost'] * storage[i, m] for i in range(OILS) for m in range(MONTHS)])

problem += profit

# Constraints
for i in range(OILS):
    # Initial Storage
    problem += storage[i, 0] == data['init_amount']
    # Final Storage
    problem += storage[i, MONTHS] == data['init_amount']
    
    for m in range(1, MONTHS + 1):
        # Balance Constraint
        if m <= MONTHS:
            problem += storage[i, m-1] + buyquantity[i, m-1] == refine[i, m-1] + storage[i, m]
        
        # Storage Capacity
        if m <= MONTHS:
            problem += storage[i, m-1] <= data['storage_size']
        
        # Usage Constraint
        if m <= MONTHS:
            problem += refine[i, m-1] >= data['min_usage'] * use[i, m-1]

# Refining Capacity Constraints
for m in range(MONTHS):
    problem += pulp.lpSum(refine[i, m] for i in range(OILS) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i, m] for i in range(OILS) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

# Hardness Constraints
for m in range(MONTHS):
    total_refine = pulp.lpSum(refine[i, m] for i in range(OILS))
    problem += pulp.lpSum((refine[i, m] / total_refine) * data['hardness'][i] for i in range(OILS)) <= data['max_hardness']
    problem += pulp.lpSum((refine[i, m] / total_refine) * data['hardness'][i] for i in range(OILS)) >= data['min_hardness']

# Usage constraint per month
for m in range(MONTHS):
    problem += pulp.lpSum(use[i, m] for i in range(OILS)) <= 3

# Dependency Constraints
for i in range(OILS):
    for j in range(OILS):
        for m in range(MONTHS):
            if data['dependencies'][i][j] == 1:
                problem += dependent_use[j, m] >= use[i, m] * data['dependencies'][i][j]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
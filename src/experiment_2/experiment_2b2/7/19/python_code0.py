import pulp

# Data from the problem
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

# Problem setup
M = len(data['buy_price'])  # Number of months
I = len(data['buy_price'][0])  # Number of oils

# Creating the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
buy = pulp.LpVariable.dicts("Buy", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0)

# Initial storage from month 0
for i in range(I):
    problem += storage[i, 0] == data['init_amount']

# Objective function
sell_price = data['sell_price']
problem += pulp.lpSum(
    sell_price * pulp.lpSum(refine[i, m] for i in range(I)) - 
    pulp.lpSum(data['buy_price'][m][i] * buy[i, m] for i in range(I)) -
    data['storage_cost'] * pulp.lpSum(storage[i, m+1] for i in range(I))
    for m in range(M)
)

# Constraints
for m in range(M):
    # Refinement capacity
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']
    
    # Hardness constraint
    total_refine = pulp.lpSum(refine[i, m] for i in range(I))
    if total_refine > 0:
        problem += pulp.lpSum(refine[i, m] * data['hardness'][i] for i in range(I)) / total_refine >= data['min_hardness']
        problem += pulp.lpSum(refine[i, m] * data['hardness'][i] for i in range(I)) / total_refine <= data['max_hardness']
    
    # Storage balance
    for i in range(I):
        problem += storage[i, m+1] == storage[i, m] + buy[i, m] - refine[i, m]
        problem += storage[i, m+1] <= data['storage_size']
    
    # Minimum usage
    for i in range(I):
        problem += refine[i, m] >= data['min_usage'] * (refine[i, m] > 0)
        
    # Maximum three oils
    problem += pulp.lpSum(refine[i, m] > 0 for i in range(I)) <= 3
    
    # Dependencies
    for i in range(I):
        for j in range(I):
            if data['dependencies'][i][j] == 1:
                problem += refine[i, m] > 0 <= (refine[j, m] > 0)

# Ending storage equals initial amounts
for i in range(I):
    problem += storage[i, M] == data['init_amount']

# Solve the problem
problem.solve()

# Fetch results
results = {
    "buy": [[pulp.value(buy[i, m]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[i, m]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[i, m]) for i in range(I)] for m in range(1, M+1)]
}

print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp
import json

# Input data
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

# Parameters
M = len(data['buy_price'])  # Number of months
I = len(data['buy_price'][0])  # Number of oils
sell_price = data['sell_price']
init_amount = data['init_amount']
min_usage = data['min_usage']
dependencies = data['dependencies']
max_veg = data['max_vegetable_refining_per_month']
max_non_veg = data['max_non_vegetable_refining_per_month']
storage_size = data['storage_size']
storage_cost = data['storage_cost']
hardness = data['hardness']
min_hardness = data['min_hardness']
max_hardness = data['max_hardness']

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
buyquantity = pulp.LpVariable.dicts("buy", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum([(sell_price * (refine[i][m] - (min_usage if m > 0 else 0))) - (data['buy_price'][m][i] * buyquantity[i][m]) - (storage_cost * storage[i][m]) 
                     for i in range(I) for m in range(M)])
problem += profit

# Constraints
for m in range(M):
    for i in range(I):
        # Storage constraints
        if m > 0:
            problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m], f"Storage_Constrain_{i}_{m}"
        else:
            problem += storage[i][m] == init_amount + buyquantity[i][m] - refine[i][m], f"Initial_Storage_Constrain_{i}_{m}"
        
    # Refining capacity constraints
    problem += pulp.lpSum(refine[i][m] for i in range(I) if data['is_vegetable'][i]) <= max_veg, f"Max_Vegetable_Refining_{m}"
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not data['is_vegetable'][i]) <= max_non_veg, f"Max_Non_Vegetable_Refining_{m}"

    # Minimum usage constraints
    for i in range(I):
        if dependencies[i].count(1) > 0:
            for j in range(I):
                if dependencies[i][j] == 1:
                    problem += refine[i][m] >= min_usage, f"Min_Usage_Constrain_{i}_{m}"
    
    # Hardness constraints
    hardness_sum = pulp.lpSum(refine[i][m] * hardness[i] for i in range(I)) / (pulp.lpSum(refine[i][m] for i in range(I)) + 1e-5)  # Adding a small value to avoid division by zero
    problem += hardness_sum >= min_hardness, f"Min_Hardness_{m}"
    problem += hardness_sum <= max_hardness, f"Max_Hardness_{m}"

# Final storage constraint to meet initial storage requirement
for i in range(I):
    problem += storage[i][M-1] == init_amount, f"Final_Storage_{i}"

# Solve the problem
problem.solve()

# Output results
buy_result = [[pulp.value(buyquantity[i][m]) for i in range(I)] for m in range(M)]
refine_result = [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)]
storage_result = [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)]

output = {
    "buy": buy_result,
    "refine": refine_result,
    "storage": storage_result
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
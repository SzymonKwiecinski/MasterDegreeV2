import pulp
import json

data = {
    'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], 
                  [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], 
                  [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 
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
    'dependencies': [[0, 0, 0, 0, 1], 
                     [0, 0, 0, 0, 1], 
                     [0, 0, 0, 0, 0], 
                     [0, 0, 0, 0, 0], 
                     [0, 0, 0, 0, 0]]
}

M = len(data['buy_price'])     # Number of months
I = len(data['buy_price'][0])  # Number of oils

# Create the LP problem
problem = pulp.LpProblem("Max_Profit", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buy", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum(data['sell_price'] * pulp.lpSum(refine[i][m] for i in range(I)) for m in range(M)) - \
                   pulp.lpSum(data['buy_price'][m][i] * buyquantity[i][m] for i in range(I) for m in range(M)) - \
                   pulp.lpSum(data['storage_cost'] * storage[i][m] for i in range(I) for m in range(M))
problem += profit

# Constraints
for m in range(M):
    for i in range(I):
        # Initial storage
        if m == 0:
            problem += storage[i][m] == data['init_amount']
        else:
            problem += storage[i][m] == storage[i][m - 1] + buyquantity[i][m] - refine[i][m]

        # Storage limit
        problem += storage[i][m] <= data['storage_size']

        # Refining constraints
        if data['is_vegetable'][i]:
            problem += refine[i][m] <= data['max_vegetable_refining_per_month']
        else:
            problem += refine[i][m] <= data['max_non_vegetable_refining_per_month']

        # Minimum usage constraint
        if (m > 0 and pulp.lpSum(refine[i][m] for i in range(I)) > 0):
            problem += pulp.lpSum(refine[i][m] for i in range(I) if data['dependencies'][i][j] == 1) >= data['min_usage']

# Hardness constraints
for m in range(M):
    problem += (pulp.lpSum(refine[i][m] * data['hardness'][i] for i in range(I)) / 
                pulp.lpSum(refine[i][m] for i in range(I))) >= data['min_hardness']
    problem += (pulp.lpSum(refine[i][m] * data['hardness'][i] for i in range(I)) / 
                pulp.lpSum(refine[i][m] for i in range(I))) <= data['max_hardness']

# Last month storage constraint
for i in range(I):
    problem += storage[i][M - 1] == data['init_amount']

# Solve the problem
problem.solve()

# Collecting results
buy = [[pulp.value(buyquantity[i][m]) for i in range(I)] for m in range(M)]
refine_result = [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)]
storage_result = [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)]

result = {
    "buy": buy,
    "refine": refine_result,
    "storage": storage_result
}

print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
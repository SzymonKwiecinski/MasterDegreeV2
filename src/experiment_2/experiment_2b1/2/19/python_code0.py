import pulp
import json

# Input data
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
    'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], 
                     [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], 
                     [0, 0, 0, 0, 0]]
}

# Parameters
I = len(data['buy_price'][0])  # Number of oils
M = len(data['buy_price'])       # Number of months

# Create the problem
problem = pulp.LpProblem("Oil_Refining_Problem", pulp.LpMaximize)

# Decision variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum(data['sell_price'] * pulp.lpSum(refine[i][m] for i in range(I)) - 
                    pulp.lpSum(data['buy_price'][m][i] * buyquantity[i][m] for i in range(I)))
problem += profit

# Constraints
for m in range(M):
    for i in range(I):
        # Storage constraints
        if m == 0:
            problem += storage[i][m] == data['init_amount']
        else:
            problem += storage[i][m] == storage[i][m - 1] + buyquantity[i][m] - refine[i][m]
        
        if m == M - 1:
            problem += storage[i][m] == data['init_amount']

    # Refining constraints
    problem += pulp.lpSum(refine[i][m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']
    
    # Hardness constraint
    hardness_avg = pulp.lpSum(data['hardness'][i] * (refine[i][m]) for i in range(I)) / (pulp.lpSum(refine[i][m] for i in range(I)) + 1e-6)
    problem += hardness_avg >= data['min_hardness']
    problem += hardness_avg <= data['max_hardness']

    # Usage constraints
    for i in range(I):
        if data['dependencies'][i][m] == 1:
            problem += refine[i][m] >= data['min_usage']

# Solve the problem
problem.solve()

# Output results
buy = [[pulp.value(buyquantity[i][m]) for i in range(I)] for m in range(M)]
refine_output = [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)]
storage_output = [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)]

output = {
    "buy": buy,
    "refine": refine_output,
    "storage": storage_output
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print results
print(json.dumps(output, indent=4))
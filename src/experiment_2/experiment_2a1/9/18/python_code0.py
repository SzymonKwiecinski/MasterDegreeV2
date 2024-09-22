import pulp
import json

# Input data
data = {
    'M': 6,
    'I': 5,
    'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], 
                  [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], 
                  [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
    'sell_price': 150,
    'is_vegetable': [True, True, False, False, False],
    'max_vegetable_refining_per_month': 200,
    'max_non_vegetable_refining_per_month': 250,
    'storage_size': 1000,
    'storage_cost': 5,
    'max_hardness': 6,
    'min_hardness': 3,
    'hardness': [8.8, 6.1, 2.0, 4.2, 5.0],
    'init_amount': 500
}

# Problem setup
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Variables
M = data['M']
I = data['I']
buyquantity = pulp.LpVariable.dicts("buy", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum((data['sell_price'] * sum(refine[i][m] for i in range(I) for m in range(M))) - 
                    pulp.lpSum(data['buy_price'][m][i] * buyquantity[i][m] for i in range(I) for m in range(M)) - 
                    pulp.lpSum(data['storage_cost'] * storage[i][m] for i in range(I) for m in range(M)))
problem += profit

# Constraints
# Initial storage
for i in range(I):
    storage[i][0] = data['init_amount']
    
# Balance constraints for storage
for m in range(1, M):
    for i in range(I):
        problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m], f"StorageBalance_{i}_{m}"

# Ending storage must equal initial amount
for i in range(I):
    problem += storage[i][M-1] == data['init_amount'], f"FinalStorage_{i}"

# Refining capacity constraints
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month'], f"MaxVegRefine_{m}"
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month'], f"MaxNonVegRefine_{m}"

# Hardness constraints
for m in range(M):
    problem += data['min_hardness'] <= (pulp.lpSum(refine[i][m] * data['hardness'][i] for i in range(I))) / pulp.lpSum(refine[i][m] for i in range(I)), f"MinHardness_{m}"
    problem += (pulp.lpSum(refine[i][m] * data['hardness'][i] for i in range(I))) / pulp.lpSum(refine[i][m] for i in range(I)) <= data['max_hardness'], f"MaxHardness_{m}"

# Solve the problem
problem.solve()

# Output results
result = {
    "buy": [[pulp.value(buyquantity[i][m]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)]
}

print(json.dumps(result, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
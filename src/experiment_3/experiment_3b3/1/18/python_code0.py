import pulp
import json

# Data from JSON
data = json.loads('''{'M': 6, 'I': 5, 'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'SellPrice': 150, 'IsVegetable': [True, True, False, False, False], 'MaxVegetableRefiningPerMonth': 200, 'MaxNonVegetableRefiningPerMonth': 250, 'StorageSize': 1000, 'StorageCost': 5, 'MinHardness': 3, 'MaxHardness': 6, 'Hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'InitialAmount': 500}''')

# Problem definition
problem = pulp.LpProblem("Oil_Refining_Company", pulp.LpMaximize)

# Parameters
M = data['M']
I = data['I']
buy_price = data['BuyPrice']
sell_price = data['SellPrice']
is_vegetable = data['IsVegetable']
max_vegetable = data['MaxVegetableRefiningPerMonth']
max_non_vegetable = data['MaxNonVegetableRefiningPerMonth']
storage_size = data['StorageSize']
storage_cost = data['StorageCost']
min_hardness = data['MinHardness']
max_hardness = data['MaxHardness']
hardness = data['Hardness']
initial_amount = data['InitialAmount']

# Decision Variables
buy_quantity = pulp.LpVariable.dicts("BuyQuantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum([sell_price * pulp.lpSum([refine[i, m] for i in range(I)]) -
                     pulp.lpSum([buy_price[m][i] * buy_quantity[i, m] for i in range(I)]) -
                     storage_cost * pulp.lpSum([storage[i, m] for i in range(I)])
                     for m in range(M)])

problem += profit

# Constraints
for i in range(I):
    # Initial storage constraint
    problem += storage[i, 0] == initial_amount

    for m in range(M):
        # Storage constraint
        problem += storage[i, m+1] == storage[i, m] + buy_quantity[i, m] - refine[i, m]

        # Storage capacity constraint
        problem += storage[i, m] <= storage_size

# Refining capacity constraints
for m in range(M):
    problem += pulp.lpSum([refine[i, m] for i in range(I) if is_vegetable[i]]) <= max_vegetable
    problem += pulp.lpSum([refine[i, m] for i in range(I) if not is_vegetable[i]]) <= max_non_vegetable

    # Hardness constraints
    total_refined = pulp.lpSum([refine[i, m] for i in range(I)])
    weighted_hardness = pulp.lpSum([hardness[i] * refine[i, m] for i in range(I)])
    problem += (total_refined * min_hardness) <= weighted_hardness
    problem += weighted_hardness <= (total_refined * max_hardness)

# Final storage constraints
for i in range(I):
    problem += storage[i, M] == initial_amount

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
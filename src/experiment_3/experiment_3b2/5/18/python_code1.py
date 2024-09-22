import pulp
import json

# Given data
data = json.loads('{"M": 6, "I": 5, "BuyPrice": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "SellPrice": 150, "IsVegetable": [true, true, false, false, false], "MaxVegetableRefiningPerMonth": 200, "MaxNonVegetableRefiningPerMonth": 250, "StorageSize": 1000, "StorageCost": 5, "MinHardness": 3, "MaxHardness": 6, "Hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "InitialAmount": 500}')

# Parameters
M = data['M']
I = data['I']
buy_price = data['BuyPrice']
sell_price = data['SellPrice']
is_vegetable = data['IsVegetable']
max_vegetable_refining_per_month = data['MaxVegetableRefiningPerMonth']
max_non_vegetable_refining_per_month = data['MaxNonVegetableRefiningPerMonth']
storage_size = data['StorageSize']
storage_cost = data['StorageCost']
min_hardness = data['MinHardness']
max_hardness = data['MaxHardness']
hardness = data['Hardness']
initial_amount = data['InitialAmount']

# Create the problem
problem = pulp.LpProblem("Oil_Refining_Problem", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, upBound=storage_size)

# Objective Function
profit = pulp.lpSum(sell_price * refine[i][m] for i in range(I) for m in range(M)) \
         - pulp.lpSum(buy_price[m][i] * buyquantity[i][m] for i in range(I) for m in range(M)) \
         - pulp.lpSum(storage_cost * storage[i][m] for i in range(I) for m in range(M))
problem += profit

# Constraints
for i in range(I):
    for m in range(M):
        if m == 0:
            problem += storage[i][m] == initial_amount + buyquantity[i][m] - refine[i][m]
        else:
            problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m]

# Final storage requirement
for i in range(I):
    problem += storage[i][M-1] == initial_amount

# Storage capacity constraints
for i in range(I):
    for m in range(M):
        problem += storage[i][m] >= 0
        problem += storage[i][m] <= storage_size

# Refining capacity constraints
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if is_vegetable[i]) <= max_vegetable_refining_per_month
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not is_vegetable[i]) <= max_non_vegetable_refining_per_month

# Hardness constraints
for m in range(M):
    total_refined = pulp.lpSum(refine[i][m] for i in range(I))
    problem += total_refined == 0 | (min_hardness <= (pulp.lpSum(hardness[i] * refine[i][m] for i in range(I)) / total_refined) <= max_hardness)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
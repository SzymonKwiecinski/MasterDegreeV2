import pulp
import json

data = json.loads('{"M": 6, "I": 5, "BuyPrice": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "SellPrice": 150, "IsVegetable": [true, true, false, false, false], "MaxVegetableRefiningPerMonth": 200, "MaxNonVegetableRefiningPerMonth": 250, "StorageSize": 1000, "StorageCost": 5, "MinHardness": 3, "MaxHardness": 6, "Hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "InitialAmount": 500}')

# Data unpacking
M = data['M']
I = data['I']
buy_price = data['BuyPrice']
sell_price = data['SellPrice']
is_vegetable = data['IsVegetable']
max_veg = data['MaxVegetableRefiningPerMonth']
max_non_veg = data['MaxNonVegetableRefiningPerMonth']
storage_size = data['StorageSize']
storage_cost = data['StorageCost']
min_hardness = data['MinHardness']
max_hardness = data['MaxHardness']
hardness = data['Hardness']
init_amount = data['InitialAmount']

# Create the LP problem
problem = pulp.LpProblem("Oil_Refinement_and_Blend", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", (range(I), range(M+1)), lowBound=0, upBound=storage_size, cat='Continuous')

# Objective Function
profit = pulp.lpSum(sell_price * pulp.lpSum(refine[i][m] for i in range(I)) for m in range(M)) \
                    - pulp.lpSum(buy_price[m][i] * buyquantity[i][m] for i in range(I) for m in range(M)) \
                    - pulp.lpSum(storage_cost * storage[i][m] for i in range(I) for m in range(M))

problem += profit

# Constraints

# Storage Constraints
for i in range(I):
    for m in range(1, M):
        problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m], f"Storage_Constraint_{i}_{m}"
    problem += storage[i][0] == init_amount, f"Initial_Storage_{i}"
    problem += storage[i][M] == init_amount, f"Final_Storage_{i}"

# Refining Capacity Constraints
for m in range(M):
    problem += pulp.lpSum(refine[i][m] for i in range(I) if is_vegetable[i]) <= max_veg, f"Max_Veg_Refining_{m}"
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not is_vegetable[i]) <= max_non_veg, f"Max_Non_Veg_Refining_{m}"

# Hardness Constraints
for m in range(M):
    refine_total = pulp.lpSum(refine[i][m] for i in range(I))
    problem += (pulp.lpSum(hardness[i] * refine[i][m] for i in range(I)) >= min_hardness * refine_total) if refine_total > 0 else 0
    problem += (pulp.lpSum(hardness[i] * refine[i][m] for i in range(I)) <= max_hardness * refine_total) if refine_total > 0 else 0

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
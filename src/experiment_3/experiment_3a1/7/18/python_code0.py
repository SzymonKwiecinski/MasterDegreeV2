import pulp
import json

# Data provided in JSON format
data_json = '''{
    "M": 6,
    "I": 5,
    "BuyPrice": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
    "SellPrice": 150,
    "IsVegetable": [true, true, false, false, false],
    "MaxVegetableRefiningPerMonth": 200,
    "MaxNonVegetableRefiningPerMonth": 250,
    "StorageSize": 1000,
    "StorageCost": 5,
    "MinHardness": 3,
    "MaxHardness": 6,
    "Hardness": [8.8, 6.1, 2.0, 4.2, 5.0],
    "InitialAmount": 500
}'''

data = json.loads(data_json)

# Parameters
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

# Create a linear programming problem
problem = pulp.LpProblem("Food_Manufacturing_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0, upBound=storage_size)

# Objective Function
profit = pulp.lpSum(sell_price * pulp.lpSum(refine[i][m] for i in range(I)) - 
                    pulp.lpSum(buy_price[m][i] * buyquantity[i][m] for i in range(I)) - 
                    storage_cost * pulp.lpSum(storage[i][m] for i in range(I))
                    for m in range(M))

problem += profit, "Total_Profit"

# Constraints
# Monthly vegetable and non-vegetable refining limits
for m in range(M):
    problem += pulp.lpSum(is_vegetable[i] * refine[i][m] for i in range(I)) <= max_veg, f"Max_Vegetable_Refining_{m}"
    problem += pulp.lpSum((1 - is_vegetable[i]) * refine[i][m] for i in range(I)) <= max_non_veg, f"Max_Non_Vegetable_Refining_{m}"

# Storage constraints
for i in range(I):
    for m in range(M):
        problem += storage[i][m] <= storage_size, f"Max_Storage_Size_{i}_{m}"
        problem += storage[i][m] >= 0, f"Min_Storage_{i}_{m}"
        if m > 0:
            problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m], f"Storage_Balance_{i}_{m}"

# Initial and final storage constraints
for i in range(I):
    problem += storage[i][0] == init_amount, f"Initial_Storage_{i}"
    problem += storage[i][M-1] == init_amount, f"Final_Storage_{i}"

# Hardness constraints
for m in range(M):
    total_refine_m = pulp.lpSum(refine[i][m] for i in range(I))
    if total_refine_m > 0:
        problem += (pulp.lpSum(hardness[i] * refine[i][m] for i in range(I)) / total_refine_m) <= max_hardness, f"Max_Hardness_{m}"
        problem += (pulp.lpSum(hardness[i] * refine[i][m] for i in range(I)) / total_refine_m) >= min_hardness, f"Min_Hardness_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
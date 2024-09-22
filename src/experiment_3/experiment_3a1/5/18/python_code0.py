import pulp
import json

# Load data
data = json.loads('{"M": 6, "I": 5, "BuyPrice": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "SellPrice": 150, "IsVegetable": [true, true, false, false, false], "MaxVegetableRefiningPerMonth": 200, "MaxNonVegetableRefiningPerMonth": 250, "StorageSize": 1000, "StorageCost": 5, "MinHardness": 3, "MaxHardness": 6, "Hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "InitialAmount": 500}')

M = data['M']
I = data['I']
BuyPrice = data['BuyPrice']
SellPrice = data['SellPrice']
IsVegetable = data['IsVegetable']
MaxVeg = data['MaxVegetableRefiningPerMonth']
MaxNonVeg = data['MaxNonVegetableRefiningPerMonth']
StorageSize = data['StorageSize']
StorageCost = data['StorageCost']
MinHardness = data['MinHardness']
MaxHardness = data['MaxHardness']
Hardness = data['Hardness']
InitialAmount = data['InitialAmount']

# Create problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(1, M+1)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(1, M+1)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0, upBound=StorageSize, cat='Continuous')

# Objective Function
profit_expr = pulp.lpSum(SellPrice * refine[i, m] for i in range(I) for m in range(1, M+1)) - \
               pulp.lpSum(BuyPrice[m-1][i] * buyquantity[i, m] for i in range(I) for m in range(1, M+1)) - \
               pulp.lpSum(StorageCost * storage[i, m] for i in range(I) for m in range(1, M+1))
problem += profit_expr

# Constraints
# Refining Capacity Constraints
for m in range(1, M+1):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if IsVegetable[i]) <= MaxVeg, f"MaxVegRefining_{m}")
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not IsVegetable[i]) <= MaxNonVeg, f"MaxNonVegRefining_{m}")

# Storage Constraints
for m in range(1, M+1):
    for i in range(I):
        problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m] - refine[i, m], f"StorageBalance_{i}_{m}"
        
# Initial and Final Storage Conditions
for i in range(I):
    problem += storage[i, 0] == InitialAmount, f"InitialStorage_{i}"
    problem += storage[i, M] == InitialAmount, f"FinalStorage_{i}"

# Hardness Constraints
for m in range(1, M+1):
    problem += (pulp.lpSum(Hardness[i] * refine[i, m] for i in range(I)) / 
                 pulp.lpSum(refine[i, m] for i in range(I)) <= MaxHardness), f"MaxHardness_{m}"
    problem += (pulp.lpSum(Hardness[i] * refine[i, m] for i in range(I)) / 
                 pulp.lpSum(refine[i, m] for i in range(I)) >= MinHardness), f"MinHardness_{m}"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
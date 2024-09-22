import pulp
import json

# Load data
data = json.loads('''{"M": 6, "I": 5, "BuyPrice": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "SellPrice": 150, "IsVegetable": [true, true, false, false, false], "MaxVegetableRefiningPerMonth": 200, "MaxNonVegetableRefiningPerMonth": 250, "StorageSize": 1000, "StorageCost": 5, "MinHardness": 3, "MaxHardness": 6, "Hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "InitialAmount": 500}''')

# Parameters
M = data['M']
I = data['I']
BuyPrice = data['BuyPrice']
SellPrice = data['SellPrice']
IsVegetable = data['IsVegetable']
MaxVegetableRefining = data['MaxVegetableRefiningPerMonth']
MaxNonVegetableRefining = data['MaxNonVegetableRefiningPerMonth']
StorageSize = data['StorageSize']
StorageCost = data['StorageCost']
MinHardness = data['MinHardness']
MaxHardness = data['MaxHardness']
Hardness = data['Hardness']
InitialAmount = data['InitialAmount']

# Problem
problem = pulp.LpProblem("Oil_Refining_and_Blending", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("BuyQuantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M + 1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(SellPrice * pulp.lpSum(refine[i, m] for i in range(I)) -
                      pulp.lpSum(BuyPrice[m][i] * buyquantity[i, m] for i in range(I)) -
                      StorageCost * pulp.lpSum(storage[i, m] for i in range(I))
                      for m in range(M))

# Constraints
for m in range(M):
    # Vegetable refining capacity
    problem += pulp.lpSum(refine[i, m] for i in range(I) if IsVegetable[i]) <= MaxVegetableRefining

    # Non-vegetable refining capacity
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not IsVegetable[i]) <= MaxNonVegetableRefining

    # Hardness constraints
    hardness_expr = pulp.lpSum(Hardness[i] * refine[i, m] for i in range(I))
    refine_sum = pulp.lpSum(refine[i, m] for i in range(I))
    problem += hardness_expr >= MinHardness * refine_sum
    problem += hardness_expr <= MaxHardness * refine_sum

    for i in range(I):
        # Storage capacity
        problem += storage[i, m] <= StorageSize

        # Storage dynamics
        if m == 0:
            problem += storage[i, m] == InitialAmount + buyquantity[i, m] - refine[i, m]
        else:
            problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m] - refine[i, m]

# Initial and final storage condition
for i in range(I):
    problem += storage[i, M] == InitialAmount

# Solve the problem
problem.solve()

# Print the objective value
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
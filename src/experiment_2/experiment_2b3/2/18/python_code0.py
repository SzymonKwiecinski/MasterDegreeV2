from pulp import LpMaximize, LpProblem, LpVariable, lpSum, value, LpStatus
import json

# Input data
data_json = '''
{'M': 6, 'I': 5, 'BuyPrice': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], 'SellPrice': 150, 'IsVegetable': [True, True, False, False, False], 'MaxVegetableRefiningPerMonth': 200, 'MaxNonVegetableRefiningPerMonth': 250, 'StorageSize': 1000, 'StorageCost': 5, 'MinHardness': 3, 'MaxHardness': 6, 'Hardness': [8.8, 6.1, 2.0, 4.2, 5.0], 'InitialAmount': 500}
'''
data = json.loads(data_json)

# Extract variables from data
M = data['M']
I = data['I']
BuyPrice = data['BuyPrice']
SellPrice = data['SellPrice']
IsVegetable = data['IsVegetable']
MaxVegetableRefiningPerMonth = data['MaxVegetableRefiningPerMonth']
MaxNonVegetableRefiningPerMonth = data['MaxNonVegetableRefiningPerMonth']
StorageSize = data['StorageSize']
StorageCost = data['StorageCost']
MinHardness = data['MinHardness']
MaxHardness = data['MaxHardness']
Hardness = data['Hardness']
InitialAmount = data['InitialAmount']

# Decision variables
buy = LpVariable.dicts("buy", (range(M), range(I)), lowBound=0)
refine = LpVariable.dicts("refine", (range(M), range(I)), lowBound=0)
storage = LpVariable.dicts("storage", (range(M+1), range(I)), lowBound=0)

# Initialize the problem
problem = LpProblem("Maximize_Profit", LpMaximize)

# Objective function
profit_terms = [
    SellPrice * lpSum(refine[m][i] for i in range(I))
    - lpSum(BuyPrice[m][i] * buy[m][i] for i in range(I))
    - StorageCost * lpSum(storage[m+1][i] for i in range(I))
    for m in range(M)
]
problem += lpSum(profit_terms)

# Initial storage
for i in range(I):
    problem += storage[0][i] == InitialAmount

# Storage transitions, refining, and refining capacity constraints
for m in range(M):
    for i in range(I):
        # Storage transition
        problem += storage[m+1][i] == storage[m][i] + buy[m][i] - refine[m][i]
        # Storage capacity
        problem += storage[m+1][i] <= StorageSize
    # Refining capacity
    problem += lpSum(refine[m][i] for i in range(I) if IsVegetable[i]) <= MaxVegetableRefiningPerMonth
    problem += lpSum(refine[m][i] for i in range(I) if not IsVegetable[i]) <= MaxNonVegetableRefiningPerMonth

# Hardness constraints
for m in range(M):
    total_refine = lpSum(refine[m][i] for i in range(I))
    if total_refine > 0:
        hardness = lpSum(Hardness[i] * refine[m][i] for i in range(I)) / total_refine
        problem += hardness >= MinHardness
        problem += hardness <= MaxHardness

# Final storage must equal initial storage
for i in range(I):
    problem += storage[M][i] == InitialAmount

# Solve the problem
problem.solve()

# Extract results
buy_result = [[buy[m][i].varValue for i in range(I)] for m in range(M)]
refine_result = [[refine[m][i].varValue for i in range(I)] for m in range(M)]
storage_result = [[storage[m][i].varValue for i in range(I)] for m in range(M+1)]

output = {
    "buy": buy_result,
    "refine": refine_result,
    "storage": storage_result
}

# Print output
print(json.dumps(output, indent=2))
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
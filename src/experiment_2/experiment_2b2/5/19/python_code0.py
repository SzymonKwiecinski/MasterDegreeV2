import pulp

# Data from the problem
data = {
    "buy_price": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
    "sell_price": 150,
    "is_vegetable": [True, True, False, False, False],
    "max_vegetable_refining_per_month": 200,
    "max_non_vegetable_refining_per_month": 250,
    "storage_size": 1000,
    "storage_cost": 5,
    "min_hardness": 3,
    "max_hardness": 6,
    "hardness": [8.8, 6.1, 2.0, 4.2, 5.0],
    "init_amount": 500,
    "min_usage": 20,
    "dependencies": [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
}

# Define indices
I = len(data["buy_price"][0])  # Number of oils
M = len(data["buy_price"])     # Number of months

# Create LP problem
problem = pulp.LpProblem("Oil_Refining_Problem", pulp.LpMaximize)

# Decision variables
buy = pulp.LpVariable.dicts("Buy", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat=pulp.LpContinuous)
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat=pulp.LpContinuous)
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0, upBound=data["storage_size"], cat=pulp.LpContinuous)

# Add initial storage constraints for month 0
for i in range(I):
    problem += (storage[i, 0] == data["init_amount"])

# Objective function: Maximize profits
profit_terms = [data["sell_price"] * pulp.lpSum(refine[i, m] for i in range(I)) -
                pulp.lpSum(data["buy_price"][m][i] * buy[i, m] for i in range(I)) -
                pulp.lpSum(data["storage_cost"] * storage[i, m] for i in range(I))
                for m in range(M)]
problem += pulp.lpSum(profit_terms)

# Constraints

# Storage balance constraints
for m in range(M):
    for i in range(I):
        problem += (storage[i, m+1] == storage[i, m] + buy[i, m] - refine[i, m])

# Refining constraints
for m in range(M):
    problem += (pulp.lpSum([(refine[i, m]) for i in range(I) if data["is_vegetable"][i]]) <= data["max_vegetable_refining_per_month"])
    problem += (pulp.lpSum([(refine[i, m]) for i in range(I) if not data["is_vegetable"][i]]) <= data["max_non_vegetable_refining_per_month"])

# Hardness constraints
for m in range(M):
    hardness = pulp.lpSum([refine[i, m] * data["hardness"][i] for i in range(I)])
    total_refined = pulp.lpSum([refine[i, m] for i in range(I)])
    problem += (hardness >= data["min_hardness"] * total_refined)
    problem += (hardness <= data["max_hardness"] * total_refined)

# Storage end constraint
for i in range(I):
    problem += (storage[i, M] == data["init_amount"])

# Maximum two oils can be used constraint
for m in range(M):
    for i in range(I):
        is_used = pulp.LpVariable(f'Is_Used_{i}_{m}', cat=pulp.LpBinary)
        problem += (refine[i, m] >= is_used * data["min_usage"])
        problem += (is_used <= pulp.lpSum([refine[i, m] for i in range(I)]) / data["min_usage"])

    problem += (pulp.lpSum([pulp.LpVariable(f'Is_Used_{i}_{m}', cat=pulp.LpBinary) for i in range(I)]) <= 3)

# Dependency constraints
for m in range(M):
    for i in range(I):
        for j in range(I):
            if data["dependencies"][i][j] == 1:
                problem += (pulp.LpVariable(f'Is_Used_{j}_{m}', cat=pulp.LpBinary) >= pulp.LpVariable(f'Is_Used_{i}_{m}', cat=pulp.LpBinary))

# Solve the problem
problem.solve()

# Output the results
buy_result = [[pulp.value(buy[i, m]) for i in range(I)] for m in range(M)]
refine_result = [[pulp.value(refine[i, m]) for i in range(I)] for m in range(M)]
storage_result = [[pulp.value(storage[i, m]) for i in range(I)] for m in range(M+1)]

result = {
    "buy": buy_result,
    "refine": refine_result,
    "storage": storage_result[:-1]  # exclude storage at month M+1 as it's not needed in the output
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
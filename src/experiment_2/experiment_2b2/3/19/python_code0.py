import pulp

# Input data
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

# Problem Parameters
I = len(data["buy_price"][0])  # Number of oils
M = len(data["buy_price"])     # Number of months

# Creating the LP Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
buy = pulp.LpVariable.dicts("Buy", (range(I), range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("Refine", (range(I), range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("Storage", (range(I), range(M+1)), lowBound=0, cat='Continuous')

# Initial storage variable
for i in range(I):
    problem += storage[i][0] == data["init_amount"]

# Objective Function: Maximize Profit
profit = pulp.lpSum(
    [data["sell_price"] * pulp.lpSum(refine[i][m] for i in range(I)) - 
     pulp.lpSum(data["buy_price"][m][i] * buy[i][m] for i in range(I)) - 
     data["storage_cost"] * pulp.lpSum(storage[i][m+1] for i in range(I))
     for m in range(M)]
)
problem += profit

# Constraints
for m in range(M):
    for i in range(I):
        # Non-negativity and storage constraints
        problem += storage[i][m+1] == storage[i][m] + buy[i][m] - refine[i][m]
        problem += storage[i][m+1] <= data["storage_size"]

    # Refining constraints
    problem += pulp.lpSum(refine[i][m] for i in range(I) if data["is_vegetable"][i]) <= data["max_vegetable_refining_per_month"]
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not data["is_vegetable"][i]) <= data["max_non_vegetable_refining_per_month"]

    # Hardness constraint
    hardness_constraint = pulp.lpSum(refine[i][m] * data["hardness"][i] for i in range(I))
    total_refine = pulp.lpSum(refine[i][m] for i in range(I))
    problem += hardness_constraint >= data["min_hardness"] * total_refine
    problem += hardness_constraint <= data["max_hardness"] * total_refine

    # At most three oils can be used
    problem += pulp.lpSum(refine[i][m] >= data["min_usage"] for i in range(I)) <= 3

    # Dependency constraints
    for i in range(I):
        for j in range(I):
            if data["dependencies"][i][j] == 1:
                problem += refine[i][m] >= data["min_usage"] * (refine[j][m] >= data["min_usage"])

# Final month storage constraint
for i in range(I):
    problem += storage[i][M] == data["init_amount"]

# Solve the problem
problem.solve()

# Extracting and printing the results
buy_quantity = [[pulp.value(buy[i][m]) for i in range(I)] for m in range(M)]
refine_quantity = [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)]
storage_quantity = [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M+1)]

result = {
    "buy": buy_quantity,
    "refine": refine_quantity,
    "storage": storage_quantity
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
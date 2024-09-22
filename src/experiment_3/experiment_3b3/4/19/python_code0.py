import pulp

# Data
data = {
    'buy_price': [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]],
    'sell_price': 150,
    'is_vegetable': [True, True, False, False, False],
    'max_vegetable_refining_per_month': 200,
    'max_non_vegetable_refining_per_month': 250,
    'storage_size': 1000,
    'storage_cost': 5,
    'min_hardness': 3,
    'max_hardness': 6,
    'hardness': [8.8, 6.1, 2.0, 4.2, 5.0],
    'init_amount': 500,
    'min_usage': 20,
    'dependencies': [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
}

I = len(data['buy_price'])        # Number of oils
M = len(data['buy_price'][0])     # Number of months

# Problem
problem = pulp.LpProblem("Oil_Blending_Problem", pulp.LpMaximize)

# Variables
buyquantity = pulp.LpVariable.dicts("BuyQuantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("Refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("Storage", ((i, m) for i in range(I) for m in range(M)), lowBound=0)

# Objective Function
profit = pulp.lpSum((data['sell_price'] * pulp.lpSum(refine[i, m] for i in range(I))) 
    - pulp.lpSum(data['buy_price'][i][m] * buyquantity[i, m] + data['storage_cost'] * storage[i, m] for i in range(I)) 
    for m in range(M))

problem += profit, "Total_Profit"

# Constraints
for m in range(M):
    # Vegetable refining constraint
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    
    # Non-vegetable refining constraint
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']
    
    # Hardness constraint
    problem += pulp.lpSum(refine[i, m] * data['hardness'][i] for i in range(I)) >= data['min_hardness'] * pulp.lpSum(refine[i, m] for i in range(I))
    problem += pulp.lpSum(refine[i, m] * data['hardness'][i] for i in range(I)) <= data['max_hardness'] * pulp.lpSum(refine[i, m] for i in range(I))
    
    # Minimum usage constraint
    for i in range(I):
        problem += refine[i, m] >= data['min_usage'] * pulp.lpSum(pulp.lpBinaryVar(f"refine_binary_{i}_{m}") for j in range(I) if refine[i, m] > 0)

    # Dependency constraint
    for i in range(I):
        for j in range(I):
            if data['dependencies'][i][j] > 0:
                problem += refine[j, m] > 0 ==> refine[i, m] > 0
    
    # No more than three oils
    problem += pulp.lpSum(pulp.lpBinaryVar(f"use_oil_{i}_{m}") for i in range(I) if refine[i, m] > 0) <= 3

# Storage and initial amount constraints
for i in range(I):
    problem += storage[i, 0] == data['init_amount'] + buyquantity[i, 0] - refine[i, 0]
    for m in range(1, M):
        problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m] - refine[i, m]
    problem += storage[i, M-1] == data['init_amount']
    for m in range(M):
        problem += storage[i, m] <= data['storage_size']

# Solve the problem
problem.solve()

# Print Objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
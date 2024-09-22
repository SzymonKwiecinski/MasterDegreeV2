import pulp
import json

# Input data from JSON
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

# Problem Definition
M = len(data['buy_price'])  # Number of months
I = len(data['buy_price'][0])  # Number of oils

problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", (range(I), range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", (range(I), range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", (range(I), range(M)), lowBound=0)

# Objective Function
problem += pulp.lpSum((data['sell_price'] * pulp.lpSum(refine[i][m] for i in range(I) for m in range(M))) -
                      pulp.lpSum(data['buy_price'][m][i] * buyquantity[i][m] for i in range(I) for m in range(M)) -
                      pulp.lpSum(data['storage_cost'] * storage[i][m] for i in range(I) for m in range(M)))

# Constraints
for m in range(M):
    # Storage constraints
    for i in range(I):
        if m == 0:
            problem += storage[i][m] == data['init_amount']  # Initial storage
        else:
            problem += storage[i][m] == storage[i][m-1] + buyquantity[i][m] - refine[i][m]  # Storage update

        # Maximum storage limit
        problem += storage[i][m] <= data['storage_size']

        # Dependencies
        for j in range(I):
            if data['dependencies'][i][j] == 1:
                problem += refine[i][m] <= refine[j][m]

    # Monthly refining limits
    problem += pulp.lpSum(refine[i][m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i][m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

    # Hardness constraints
    problem += (pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) / 
                 pulp.lpSum(refine[i][m] for i in range(I))) >= data['min_hardness']
    problem += (pulp.lpSum(data['hardness'][i] * refine[i][m] for i in range(I)) / 
                 pulp.lpSum(refine[i][m] for i in range(I))) <= data['max_hardness']

    # Minimum usage constraint
    for i in range(I):
        problem += refine[i][m] >= data['min_usage'] * (refine[i][m] > 0)

# Storage balance constraint at last month
for i in range(I):
    problem += storage[i][M-1] == data['init_amount']

# Solve the problem
problem.solve()

# Prepare output data
output = {
    "buy": [[pulp.value(buyquantity[i][m]) for i in range(I)] for m in range(M)],
    "refine": [[pulp.value(refine[i][m]) for i in range(I)] for m in range(M)],
    "storage": [[pulp.value(storage[i][m]) for i in range(I)] for m in range(M)],
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Print the output
print(json.dumps(output))
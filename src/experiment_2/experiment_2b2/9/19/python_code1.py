from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpBinary, LpStatus, value
import json

# Load data
data = json.loads('''{"buy_price": [[110, 120, 130, 110, 115], [130, 130, 110, 90, 115], [110, 140, 130, 100, 95], [120, 110, 120, 120, 125], [100, 120, 150, 110, 105], [90, 100, 140, 80, 135]], "sell_price": 150, "is_vegetable": [true, true, false, false, false], "max_vegetable_refining_per_month": 200, "max_non_vegetable_refining_per_month": 250, "storage_size": 1000, "storage_cost": 5, "min_hardness": 3, "max_hardness": 6, "hardness": [8.8, 6.1, 2.0, 4.2, 5.0], "init_amount": 500, "min_usage": 20, "dependencies": [[0, 0, 0, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]}''')

I = len(data['is_vegetable'])
M = len(data['buy_price'])

# Problem
problem = LpProblem("Maximize_Profit", LpMaximize)

# Decision variables
buy = LpVariable.dicts("Buy", (range(M), range(I)), lowBound=0)
refine = LpVariable.dicts("Refine", (range(M), range(I)), lowBound=0)
storage = LpVariable.dicts("Storage", (range(M + 1), range(I)), lowBound=0)
use_flag = LpVariable.dicts("UseFlag", (range(M), range(I)), cat=LpBinary)

# Adding initial storage
for i in range(I):
    storage[0][i] = data['init_amount']

# Objective function
problem += lpSum(
    (data['sell_price'] - data['buy_price'][m][i]) * refine[m][i]
    - data['storage_cost'] * storage[m + 1][i]
    for m in range(M) 
    for i in range(I)
)

# Constraints
for m in range(M):
    problem += lpSum(refine[m][i] * data['hardness'][i] for i in range(I)) >= data['min_hardness'] * lpSum(refine[m][i] for i in range(I))
    problem += lpSum(refine[m][i] * data['hardness'][i] for i in range(I)) <= data['max_hardness'] * lpSum(refine[m][i] for i in range(I))
    problem += lpSum(refine[m][i] for i in range(I)) <= 450  # Combined refining limit

    problem += lpSum(refine[m][i] for i, v in enumerate(data['is_vegetable']) if v) <= data['max_vegetable_refining_per_month']
    problem += lpSum(refine[m][i] for i, v in enumerate(data['is_vegetable']) if not v) <= data['max_non_vegetable_refining_per_month']

    for i in range(I):
        problem += storage[m + 1][i] == storage[m][i] + buy[m][i] - refine[m][i]
        problem += storage[m + 1][i] <= data['storage_size']

        problem += refine[m][i] >= data['min_usage'] * use_flag[m][i]
        problem += lpSum(use_flag[m][i] for i in range(I)) <= 3
        for j in range(I):
            problem += use_flag[m][i] <= use_flag[m][j] + (1 - data['dependencies'][i][j])
            
for i in range(I):
    problem += storage[M][i] == data['init_amount']

# Solve problem
problem.solve()

# Output results
output = {
    "buy": [[buy[m][i].varValue for i in range(I)] for m in range(M)],
    "refine": [[refine[m][i].varValue for i in range(I)] for m in range(M)],
    "storage": [[storage[m][i].varValue if m > 0 else storage[0][i] for i in range(I)] for m in range(M + 1)]
}

# Print the output and objective value
print(json.dumps(output, indent=2))
print(f' (Objective Value): <OBJ>{value(problem.objective)}</OBJ>')
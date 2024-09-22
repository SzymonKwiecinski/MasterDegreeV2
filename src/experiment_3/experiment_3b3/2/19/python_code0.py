import pulp

# Data provided
data = {
    'buy_price': [[110, 120, 130, 110, 115], 
                  [130, 130, 110, 90, 115], 
                  [110, 140, 130, 100, 95], 
                  [120, 110, 120, 120, 125], 
                  [100, 120, 150, 110, 105], 
                  [90, 100, 140, 80, 135]], 
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
    'dependencies': [
        [0, 0, 0, 0, 1], 
        [0, 0, 0, 0, 1], 
        [0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0], 
        [0, 0, 0, 0, 0]
    ]
}

# Sets
I = len(data['is_vegetable'])
M = len(data['buy_price'][0])

# Creating the problem variable
problem = pulp.LpProblem("Oil_Refining_Problem", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0)
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0)

# Objective Function
problem += pulp.lpSum(
    data['sell_price'] * refine[i, m] - 
    buyquantity[i, m] * data['buy_price'][i][m] -
    storage[i, m] * data['storage_cost']
    for i in range(I) for m in range(M)
)

# Constraints
# Refining Limitations
for m in range(M):
    problem += pulp.lpSum(refine[i, m] for i in range(I) if data['is_vegetable'][i]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum(refine[i, m] for i in range(I) if not data['is_vegetable'][i]) <= data['max_non_vegetable_refining_per_month']

# Storage Limitations
for i in range(I):
    for m in range(M):
        problem += storage[i, m] <= data['storage_size']

# Initial and Final Storage Condition
for i in range(I):
    problem += storage[i, 0] == data['init_amount']
    problem += storage[i, M] == data['init_amount']

# Hardness Constraint
for m in range(M):
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) >= data['min_hardness'] * pulp.lpSum(refine[i, m] for i in range(I))
    problem += pulp.lpSum(data['hardness'][i] * refine[i, m] for i in range(I)) <= data['max_hardness'] * pulp.lpSum(refine[i, m] for i in range(I))

# Dependency Condition
for m in range(M):
    for i in range(I):
        if any(data['dependencies'][i][j] for j in range(I)):
            for j in range(I):
                if data['dependencies'][i][j]:
                    problem += refine[j, m] >= data['min_usage'] * pulp.lpSum(refine[i, m] > 0 for i in range(I))

# Storage Update Equation
for i in range(I):
    for m in range(1, M+1):
        problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m-1] - refine[i, m-1]

# Oil Usage Limitation
for m in range(M):
    problem += pulp.lpSum(pulp.lpBinary(refine[i, m] > 0) for i in range(I)) <= 3

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
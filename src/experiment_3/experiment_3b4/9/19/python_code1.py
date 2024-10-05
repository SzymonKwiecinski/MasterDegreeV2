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

# Indices
I = len(data['buy_price'])
M = len(data['buy_price'][0])

# Problem
problem = pulp.LpProblem("Oil_Refining_And_Blending", pulp.LpMaximize)

# Decision Variables
buyquantity = pulp.LpVariable.dicts("buyquantity", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
refine = pulp.LpVariable.dicts("refine", ((i, m) for i in range(I) for m in range(M)), lowBound=0, cat='Continuous')
storage = pulp.LpVariable.dicts("storage", ((i, m) for i in range(I) for m in range(M+1)), lowBound=0, cat='Continuous')
use = pulp.LpVariable.dicts("use", ((i, m) for i in range(I) for m in range(M)), cat='Binary')

# Objective Function
profit = pulp.lpSum([data['sell_price'] * pulp.lpSum([refine[i, m] for i in range(I)]) -
                     pulp.lpSum([data['buy_price'][i][m] * buyquantity[i, m] for i in range(I)]) -
                     data['storage_cost'] * pulp.lpSum([storage[i, m] for i in range(I)]) for m in range(M)])
problem += profit

# Constraints
for i in range(I):
    for m in range(M):
        if m == 0:
            problem += storage[i, m] == data['init_amount'] + buyquantity[i, m] - refine[i, m]
        else:
            problem += storage[i, m] == storage[i, m-1] + buyquantity[i, m] - refine[i, m]
        
        problem += storage[i, m] <= data['storage_size']
        problem += use[i, m] * data['min_usage'] <= refine[i, m]

problem += pulp.lpSum([use[i, m] for i in range(I) for m in range(M)]) <= 3

for m in range(M):
    problem += pulp.lpSum([refine[i, m] for i in range(I) if data['is_vegetable'][i]]) <= data['max_vegetable_refining_per_month']
    problem += pulp.lpSum([refine[i, m] for i in range(I) if not data['is_vegetable'][i]]) <= data['max_non_vegetable_refining_per_month']
    
    refine_sum = pulp.lpSum([refine[i, m] for i in range(I)])
    problem += (refine_sum > 0)  # This line added for the next constraints to be valid
    problem += data['min_hardness'] <= pulp.lpSum([data['hardness'][i] * refine[i, m] for i in range(I)]) / (refine_sum + 1e-10)
    problem += pulp.lpSum([data['hardness'][i] * refine[i, m] for i in range(I)]) / (refine_sum + 1e-10) <= data['max_hardness']

for i in range(I):
    for j in range(I):
        if data['dependencies'][i][j] == 1:
            for m in range(M):
                problem += use[i, m] * data['dependencies'][i][j] <= use[j, m]

problem.solve()

print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
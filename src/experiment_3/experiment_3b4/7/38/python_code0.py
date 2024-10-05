import pulp

# Data
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
N = len(demand)

# Problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
inv = [pulp.LpVariable(f'inv_{n}', lowBound=0) for n in range(N)]

# Objective Function
problem += pulp.lpSum([cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inv[n] for n in range(N)])

# Constraints
inv_0 = 0
for n in range(N):
    inv_prev = inv_0 if n == 0 else inv[n-1]
    problem += (reg_quant[n] + over_quant[n] + inv_prev == demand[n] + inv[n], f'Balance_{n}')
    problem += (reg_quant[n] <= max_regular_amount, f'Max_Regular_{n}')

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
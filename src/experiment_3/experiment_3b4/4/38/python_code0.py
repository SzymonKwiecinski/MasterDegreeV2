import pulp

# Data
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

# Variables
N = len(data['demand'])
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Problem
problem = pulp.LpProblem("Minimize_Total_Cost", pulp.LpMinimize)

# Decision Variables
reg_quant = pulp.LpVariable.dicts("Regular_Quantity", range(N), lowBound=0, cat='Continuous')
over_quant = pulp.LpVariable.dicts("Overtime_Quantity", range(N), lowBound=0, cat='Continuous')
store_quant = pulp.LpVariable.dicts("Storage_Quantity", range(N), lowBound=0, cat='Continuous')

# Objective
problem += pulp.lpSum([
    cost_regular * reg_quant[n] + 
    cost_overtime * over_quant[n] + 
    store_cost * store_quant[n] for n in range(N)
])

# Constraints
for n in range(N):
    if n == 0:
        store_quant_prev = 0
    else:
        store_quant_prev = store_quant[n-1]
    
    # Demand Satisfaction
    problem += reg_quant[n] + over_quant[n] + store_quant_prev == demand[n] + store_quant[n]
    
    # Regular Production Limit
    problem += reg_quant[n] <= max_regular_amount

# Solve
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
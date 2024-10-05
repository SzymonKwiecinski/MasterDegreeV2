import pulp

# Data provided
data = {'demand': [10.0, 20.0, 10.0], 
        'max_regular_amount': 5.0, 
        'cost_regular': 10.0, 
        'cost_overtime': 12.0, 
        'store_cost': 1.0}

# Parameters
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
N = len(demand)

# Problem definition
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n+1}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n+1}', lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f'inventory_{n+1}', lowBound=0) for n in range(N)]

# Objective Function
problem += pulp.lpSum(
    cost_regular * reg_quant[n] + 
    cost_overtime * over_quant[n] + 
    store_cost * inventory[n] for n in range(N)
)

# Constraints
for n in range(N):
    if n == 0:
        # For the first month, assume initial inventory is zero
        problem += reg_quant[n] + over_quant[n] - inventory[n] == demand[n]
    else:
        problem += reg_quant[n] + over_quant[n] + inventory[n-1] - inventory[n] == demand[n]

    problem += reg_quant[n] <= max_regular_amount

# Solve the Problem
problem.solve()

# Output results
reg_quant_output = [pulp.value(reg_quant[n]) for n in range(N)]
over_quant_output = [pulp.value(over_quant[n]) for n in range(N)]

print(f'Regular Production Quantities: {reg_quant_output}')
print(f'Overtime Production Quantities: {over_quant_output}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
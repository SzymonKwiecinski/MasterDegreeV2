import pulp

# Data from the JSON format
data = {'demand': [10.0, 20.0, 10.0], 
        'max_regular_amount': 5.0, 
        'cost_regular': 10.0, 
        'cost_overtime': 12.0, 
        'store_cost': 1.0}

# Extracting parameters
demand = data['demand']
N = len(demand)
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Defining the problem
problem = pulp.LpProblem("Production_Schedule_Optimization", pulp.LpMinimize)

# Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0, cat='Continuous') for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0, cat='Continuous') for n in range(N)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0, cat='Continuous') for n in range(N)]

# Constraints
for n in range(N):
    if n == 0:
        prev_inventory = 0  # inventory_0 = 0
    else:
        prev_inventory = inventory[n-1]
    
    # Inventory balance constraint
    problem += reg_quant[n] + over_quant[n] + prev_inventory == demand[n] + inventory[n]
    
    # Maximum regular production constraint
    problem += reg_quant[n] <= max_regular_amount

# Objective function
problem += pulp.lpSum(
    cost_regular * reg_quant[n] + 
    cost_overtime * over_quant[n] + 
    store_cost * inventory[n]
    for n in range(N)
)

# Solve the problem
problem.solve()

# Output
reg_quant_values = [reg_quant[n].varValue for n in range(N)]
over_quant_values = [over_quant[n].varValue for n in range(N)]

print('Regular Production Quantities:', reg_quant_values)
print('Overtime Production Quantities:', over_quant_values)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
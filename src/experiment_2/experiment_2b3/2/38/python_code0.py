import pulp

# Data
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}

demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
months = len(demand)

# Problem
problem = pulp.LpProblem("Production_Schedule", pulp.LpMinimize)

# Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{i+1}', lowBound=0) for i in range(months)]
over_quant = [pulp.LpVariable(f'over_quant_{i+1}', lowBound=0) for i in range(months)]
storage = [pulp.LpVariable(f'storage_{i+1}', lowBound=0) for i in range(months)]

# Objective Function
cost = (pulp.lpSum(cost_regular * reg_quant[i] for i in range(months)) +
        pulp.lpSum(cost_overtime * over_quant[i] for i in range(months)) +
        pulp.lpSum(store_cost * storage[i] for i in range(months)))

problem += cost

# Constraints
for i in range(months):
    # Meeting demand constraints
    produced = reg_quant[i] + over_quant[i]
    if i == 0:
        problem += (produced + storage[i] == demand[i])
    else:
        problem += (produced + storage[i-1] - storage[i] == demand[i])
    
    # Regular production limit
    problem += (reg_quant[i] <= max_regular_amount)

# Solve
problem.solve()

# Output format
output = {
    "reg_quant": [pulp.value(reg_quant[i]) for i in range(months)],
    "over_quant": [pulp.value(over_quant[i]) for i in range(months)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
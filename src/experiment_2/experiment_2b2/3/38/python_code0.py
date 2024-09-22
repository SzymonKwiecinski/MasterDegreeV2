import pulp

# Parse the input data
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Number of months
months = len(demand)

# Initialize the problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision variables
regular_production = [pulp.LpVariable(f'regular_{n}', lowBound=0) for n in range(months)]
overtime_production = [pulp.LpVariable(f'overtime_{n}', lowBound=0) for n in range(months)]
storage = [pulp.LpVariable(f'storage_{n}', lowBound=0) for n in range(months)]

# Objective function
problem += pulp.lpSum([
    cost_regular * regular_production[n] + 
    cost_overtime * overtime_production[n] + 
    store_cost * storage[n]
    for n in range(months)
])

# Constraints
for n in range(months):
    # Regular production limit
    problem += regular_production[n] <= max_regular_amount
    
    # Demand satisfaction constraint
    if n == 0:
        problem += regular_production[n] + overtime_production[n] == demand[n] + storage[n]
    else:
        problem += regular_production[n] + overtime_production[n] + storage[n-1] == demand[n] + storage[n]

# Solve the problem
problem.solve()

# Output
output = {
    "reg_quant": [regular_production[n].varValue for n in range(months)],
    "over_quant": [overtime_production[n].varValue for n in range(months)]
}

print(output)

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
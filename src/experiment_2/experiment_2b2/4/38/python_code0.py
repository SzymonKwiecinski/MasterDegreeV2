import pulp

# Data input
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

# Extracting data
demands = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

months = len(demands)

# Define the LP problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0, cat='Continuous') for n in range(months)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0, cat='Continuous') for n in range(months)]
store_units = [pulp.LpVariable(f'store_units_{n}', lowBound=0, cat='Continuous') for n in range(months)]

# Objective function
problem += pulp.lpSum([cost_regular * reg_quant[n] + 
                       cost_overtime * over_quant[n] + 
                       store_cost * store_units[n] for n in range(months)])

# Constraints
for n in range(months):
    # Satisfying demand
    if n == 0:
        problem += reg_quant[n] + over_quant[n] == demands[n] + store_units[n]
    else:
        problem += reg_quant[n] + over_quant[n] + store_units[n-1] == demands[n] + store_units[n]
    
    # Regular production limit
    problem += reg_quant[n] <= max_regular_amount

# Solve the problem
problem.solve()

# Prepare output
output = {
    "reg_quant": [pulp.value(reg_quant[n]) for n in range(months)],
    "over_quant": [pulp.value(over_quant[n]) for n in range(months)]
}

print(output)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
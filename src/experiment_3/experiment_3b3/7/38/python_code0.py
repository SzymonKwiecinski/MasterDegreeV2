import pulp

# Data from JSON format
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}

# Parameters
demands = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
N = len(demands)

# Define the problem
problem = pulp.LpProblem("ProductionScheduleOptimization", pulp.LpMinimize)

# Decision Variables
reg_quant = pulp.LpVariable.dicts("reg_quant", range(N), lowBound=0)
over_quant = pulp.LpVariable.dicts("over_quant", range(N), lowBound=0)
inventory = pulp.LpVariable.dicts("inventory", range(N), lowBound=0)

# Objective Function
problem += pulp.lpSum([cost_regular * reg_quant[n] + 
                       cost_overtime * over_quant[n] + 
                       store_cost * inventory[n] 
                       for n in range(N)])

# Constraints
for n in range(N):
    if n == 0:
        problem += inventory[n] == reg_quant[n] + over_quant[n] - demands[n]
    else:
        problem += inventory[n] == inventory[n-1] + reg_quant[n] + over_quant[n] - demands[n]
    problem += reg_quant[n] <= max_regular_amount

# Solve the problem
problem.solve()

# Output results
reg_quant_solution = [pulp.value(reg_quant[n]) for n in range(N)]
over_quant_solution = [pulp.value(over_quant[n]) for n in range(N)]

print(f'Regular Production Quantities: {reg_quant_solution}')
print(f'Overtime Production Quantities: {over_quant_solution}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
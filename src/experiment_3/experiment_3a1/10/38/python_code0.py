import pulp

# Data from JSON
data = {'demand': [10.0, 20.0, 10.0], 
        'max_regular_amount': 5.0, 
        'cost_regular': 10.0, 
        'cost_overtime': 12.0, 
        'store_cost': 1.0}

N = len(data['demand'])
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Create the problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0, upBound=max_regular_amount) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(N)]

# Objective function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inventory[n] for n in range(N))

# Constraints
# Inventory balance constraints
for n in range(N):
    if n == 0:
        problem += reg_quant[n] + over_quant[n] - inventory[n] == demand[n], f"Demand_Constraint_{n}"
    else:
        problem += reg_quant[n] + over_quant[n] + inventory[n-1] - inventory[n] == demand[n], f"Demand_Constraint_{n}"

# Maximum regular production constraints
for n in range(N):
    problem += reg_quant[n] <= max_regular_amount, f"Max_Regular_Production_{n}"

# Solve the problem
problem.solve()

# Output results
reg_quant_result = [reg_quant[n].varValue for n in range(N)]
over_quant_result = [over_quant[n].varValue for n in range(N)]

print(f'Regular Production Quantities: {reg_quant_result}')
print(f'Overtime Production Quantities: {over_quant_result}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
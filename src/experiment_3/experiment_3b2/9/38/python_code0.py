import pulp

# Data from JSON
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

N = len(data['demand'])
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Create the linear programming problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
store = [pulp.LpVariable(f'store_{n}', lowBound=0) for n in range(N)]

# Objective Function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * store[n] for n in range(N))

# Constraints
store_previous = 0
for n in range(N):
    # Demand satisfaction constraint
    problem += reg_quant[n] + over_quant[n] + store_previous == demand[n] + store[n], f'Demand_Constraint_{n}'
    
    # Regular production limit constraint
    problem += reg_quant[n] <= max_regular_amount, f'Regular_Production_Limit_{n}'
    
    # Update for the next month's storage
    store_previous = store[n]

# Solve the problem
problem.solve()

# Output the results
for n in range(N):
    print(f'Regular production for month {n + 1}: {reg_quant[n].varValue}')
    print(f'Overtime production for month {n + 1}: {over_quant[n].varValue}')
    
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
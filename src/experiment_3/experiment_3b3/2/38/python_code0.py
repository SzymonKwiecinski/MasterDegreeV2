import pulp

# Data input
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

demand = data['demand']
N = len(demand)
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Create a LP minimization problem
problem = pulp.LpProblem("Production_Scheduling_Problem", pulp.LpMinimize)

# Decision Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(N)]

# Objective Function
problem += pulp.lpSum([
    cost_regular * reg_quant[n] + 
    cost_overtime * over_quant[n] + 
    store_cost * inventory[n]
    for n in range(N)
])

# Constraints
# Initial inventory constraint
problem += inventory[0] == 0

# Production and inventory constraints
for n in range(N):
    if n == 0:
        problem += reg_quant[n] + over_quant[n] >= demand[n]
    else:
        problem += reg_quant[n] + over_quant[n] + inventory[n-1] >= demand[n]
        problem += inventory[n] == inventory[n-1] + reg_quant[n] + over_quant[n] - demand[n]
    
    problem += reg_quant[n] <= max_regular_amount

# Solve the problem
problem.solve()

# Output the results
for n in range(N):
    print(f'Month {n+1}: Regular Quant = {reg_quant[n].varValue}, Overtime Quant = {over_quant[n].varValue}, Inventory = {inventory[n].varValue}')

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
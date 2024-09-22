import pulp

# Data from the JSON input
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}

# Extracting individual parameters from data
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
N = len(demand)  # Number of months

# Defining the problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(N+1)]

# Objective Function: Minimize total costs
problem += pulp.lpSum([
    cost_regular * reg_quant[n] +
    cost_overtime * over_quant[n] +
    store_cost * inventory[n+1]
    for n in range(N)
])

# Constraints
for n in range(N):
    # Satisfy demand from production and inventory
    if n == 0:
        problem += reg_quant[n] + over_quant[n] == demand[n] + inventory[n+1]
    else:
        problem += reg_quant[n] + over_quant[n] + inventory[n] == demand[n] + inventory[n+1]
    
    # Regular production limit
    problem += reg_quant[n] <= max_regular_amount

# Initial inventory is zero
problem += inventory[0] == 0

# Solve the problem
problem.solve()

# Output results
result = {
    "reg_quant": [pulp.value(reg_quant[n]) for n in range(N)],
    "over_quant": [pulp.value(over_quant[n]) for n in range(N)]
}
print(result)
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
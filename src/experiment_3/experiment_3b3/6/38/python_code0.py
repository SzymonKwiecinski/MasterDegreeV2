import pulp

# Input data
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

# Parameters
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
N = len(demand)

# Problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Variables
reg_quant = [pulp.LpVariable(f"reg_quant_{n}", lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f"over_quant_{n}", lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f"inventory_{n}", lowBound=0) for n in range(N)]

# Objective Function
problem += pulp.lpSum(
    cost_regular * reg_quant[n] +
    cost_overtime * over_quant[n] +
    store_cost * inventory[n]
    for n in range(N)
), "Total Cost"

# Constraints
# Initial Inventory
problem += inventory[0] == 0, "Initial Inventory"

# Demand satisfaction and inventory balance
for n in range(N):
    if n == 0:
        prev_inventory = 0
    else:
        prev_inventory = inventory[n-1]
    
    problem += prev_inventory + reg_quant[n] + over_quant[n] >= demand[n], f"Demand Satisfaction Month {n+1}"
    problem += inventory[n] == prev_inventory + reg_quant[n] + over_quant[n] - demand[n], f"Inventory Balance Month {n+1}"

# Regular Production Limit
for n in range(N):
    problem += reg_quant[n] <= max_regular_amount, f"Regular Production Limit Month {n+1}"

# Solve the problem
problem.solve()

# Output results
output = {
    "reg_quant": [pulp.value(reg_quant[n]) for n in range(N)],
    "over_quant": [pulp.value(over_quant[n]) for n in range(N)]
}

print("Output:", output)
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
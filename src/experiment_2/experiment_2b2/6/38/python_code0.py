import pulp

# Data from input
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Number of months
N = len(demand)

# Create a LP Minimization problem
problem = pulp.LpProblem("Minimize_Costs", pulp.LpMinimize)

# Decision Variables
reg_production = [pulp.LpVariable(f"reg_production_{n}", lowBound=0) for n in range(N)]
over_production = [pulp.LpVariable(f"over_production_{n}", lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f"inventory_{n}", lowBound=0) for n in range(N)]

# Objective Function
problem += pulp.lpSum([
    cost_regular * reg_production[n] +
    cost_overtime * over_production[n] +
    store_cost * inventory[n]
    for n in range(N)
])

# Constraints
# Satisfy demand for each month
for n in range(N):
    if n == 0:
        problem += reg_production[n] + over_production[n] - inventory[n] == demand[n]
    else:
        problem += reg_production[n] + over_production[n] + inventory[n-1] - inventory[n] == demand[n]

# Regular production cannot exceed max regular production
for n in range(N):
    problem += reg_production[n] <= max_regular_amount

# Solve the problem
problem.solve()

# Output results
reg_quant = [pulp.value(reg_production[n]) for n in range(N)]
over_quant = [pulp.value(over_production[n]) for n in range(N)]
output = {
    "reg_quant": reg_quant,
    "over_quant": over_quant
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
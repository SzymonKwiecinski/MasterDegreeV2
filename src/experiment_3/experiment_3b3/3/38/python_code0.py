import pulp

# Extract data from the provided JSON structure
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

# Define problem
problem = pulp.LpProblem("Production_Scheduling_Problem", pulp.LpMinimize)

# Number of months
N = len(data['demand'])

# Decision Variables
reg_quant = [pulp.LpVariable(f"reg_quant_{n+1}", lowBound=0, cat='Continuous') for n in range(N)]
over_quant = [pulp.LpVariable(f"over_quant_{n+1}", lowBound=0, cat='Continuous') for n in range(N)]
inventory = [pulp.LpVariable(f"inventory_{n+1}", lowBound=0, cat='Continuous') for n in range(N)]

# Objective Function
problem += pulp.lpSum([
    data['cost_regular'] * reg_quant[n] +
    data['cost_overtime'] * over_quant[n] +
    data['store_cost'] * inventory[n]
    for n in range(N)
])

# Constraints

# Initial inventory
inventory_0 = 0

# Demand Satisfaction Constraint
for n in range(N):
    if n == 0:
        inventory_prev = inventory_0
    else:
        inventory_prev = inventory[n-1]

    problem += (reg_quant[n] + over_quant[n] + inventory_prev - inventory[n] == data['demand'][n])

# Regular Production Limit Constraint
for n in range(N):
    problem += (reg_quant[n] <= data['max_regular_amount'])

# Solve the problem
problem.solve()

# Output Results
reg_result = [pulp.value(reg_quant[n]) for n in range(N)]
over_result = [pulp.value(over_quant[n]) for n in range(N)]

output = {
    "reg_quant": reg_result,
    "over_quant": over_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
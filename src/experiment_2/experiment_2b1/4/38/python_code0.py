import pulp
import json

# Input data
data = json.loads('{"demand": [10.0, 20.0, 10.0], "max_regular_amount": 5.0, "cost_regular": 10.0, "cost_overtime": 12.0, "store_cost": 1.0}')

# Unpacking data
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
n_months = len(demand)

# Create the problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision variables
reg_quant = [pulp.LpVariable(f'reg_quant_{i}', lowBound=0, upBound=max_regular_amount, cat='Continuous') for i in range(n_months)]
over_quant = [pulp.LpVariable(f'over_quant_{i}', lowBound=0, cat='Continuous') for i in range(n_months)]
inventory = [pulp.LpVariable(f'inventory_{i}', lowBound=0, cat='Continuous') for i in range(n_months)]

# Objective function
problem += pulp.lpSum(cost_regular * reg_quant[i] + cost_overtime * over_quant[i] + store_cost * inventory[i] for i in range(n_months))

# Constraints
for i in range(n_months):
    if i == 0:
        problem += reg_quant[i] + over_quant[i] - demand[i] + inventory[i] == 0
    else:
        problem += reg_quant[i] + over_quant[i] + inventory[i-1] - demand[i] + inventory[i] == 0

for i in range(n_months):
    if i > 0:
        problem += inventory[i] >= 0

# Solve the problem
problem.solve()

# Extract the results
reg_quant_values = [pulp.value(var) for var in reg_quant]
over_quant_values = [pulp.value(var) for var in over_quant]

# Output the results
output = {
    "reg_quant": reg_quant_values,
    "over_quant": over_quant_values
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
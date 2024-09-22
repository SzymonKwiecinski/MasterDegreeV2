import pulp
import json

# Input data
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}

# Problem variables
demand = data['demand']
max_regular = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
n = len(demand)

# Define the problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision variables
reg_quant = [pulp.LpVariable(f'reg_quant_{i}', lowBound=0, upBound=max_regular, cat='Continuous') for i in range(n)]
over_quant = [pulp.LpVariable(f'over_quant_{i}', lowBound=0, cat='Continuous') for i in range(n)]
inventory = [pulp.LpVariable(f'inventory_{i}', lowBound=0, cat='Continuous') for i in range(n)]

# Objective function
total_cost = (
    pulp.lpSum(cost_regular * reg_quant[i] for i in range(n)) +
    pulp.lpSum(cost_overtime * over_quant[i] for i in range(n)) +
    pulp.lpSum(store_cost * inventory[i] for i in range(n))
)
problem += total_cost

# Constraints
for i in range(n):
    # Inventory balance constraints
    if i == 0:
        problem += (reg_quant[i] + over_quant[i] - demand[i] == inventory[i])
    else:
        problem += (reg_quant[i] + over_quant[i] + inventory[i-1] - demand[i] == inventory[i])

# Solve the problem
problem.solve()

# Output results
reg_quant_values = [pulp.value(reg_quant[i]) for i in range(n)]
over_quant_values = [pulp.value(over_quant[i]) for i in range(n)]

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Format output
output = {
    "reg_quant": reg_quant_values,
    "over_quant": over_quant_values
}

print(output)
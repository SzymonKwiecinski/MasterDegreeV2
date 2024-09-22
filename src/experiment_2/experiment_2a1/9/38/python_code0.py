import pulp
import json

# Input data
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}

# Extracting values from the data
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
n = len(demand)

# Define the problem
problem = pulp.LpProblem("Minimize_Cost", pulp.LpMinimize)

# Decision Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{i}', lowBound=0, upBound=max_regular_amount, cat='Continuous') for i in range(n)]
over_quant = [pulp.LpVariable(f'over_quant_{i}', lowBound=0, cat='Continuous') for i in range(n)]
inventory = [pulp.LpVariable(f'inventory_{i}', lowBound=0, cat='Continuous') for i in range(n)]

# Objective Function
problem += pulp.lpSum(cost_regular * reg_quant[i] + cost_overtime * over_quant[i] + store_cost * inventory[i] for i in range(n))

# Constraints
for i in range(n):
    if i == 0:
        problem += reg_quant[i] + over_quant[i] - demand[i] == inventory[i]
    else:
        problem += reg_quant[i] + over_quant[i] + inventory[i-1] - demand[i] == inventory[i]

# Solve the problem
problem.solve()

# Prepare the output
reg_quant_values = [reg_quant[i].varValue for i in range(n)]
over_quant_values = [over_quant[i].varValue for i in range(n)]

# Output the results
output = {
    "reg_quant": reg_quant_values,
    "over_quant": over_quant_values
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
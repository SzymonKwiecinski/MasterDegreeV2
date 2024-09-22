import pulp
import json

# Input data
data = json.loads('{"demand": [10.0, 20.0, 10.0], "max_regular_amount": 5.0, "cost_regular": 10.0, "cost_overtime": 12.0, "store_cost": 1.0}')

# Parameters
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
n_months = len(demand)

# Create problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0, upBound=max_regular_amount, cat='Continuous') for n in range(n_months)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0, cat='Continuous') for n in range(n_months)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0, cat='Continuous') for n in range(n_months + 1)]

# Objective function
cost = pulp.lpSum([reg_quant[n] * cost_regular + over_quant[n] * cost_overtime + inventory[n] * store_cost for n in range(n_months)]) 
problem += cost

# Constraints
# Inventory balance
for n in range(n_months):
    if n == 0:
        problem += inventory[n] + reg_quant[n] + over_quant[n] == demand[n], f"Balance_Constraint_{n}"
    else:
        problem += inventory[n-1] + reg_quant[n] + over_quant[n] == demand[n] + inventory[n], f"Balance_Constraint_{n}"

# Define the objective
problem += cost

# Solve
problem.solve()

# Prepare output
output = {
    "reg_quant": [pulp.value(reg_quant[n]) for n in range(n_months)],
    "over_quant": [pulp.value(over_quant[n]) for n in range(n_months)]
}

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output result
print(json.dumps(output))
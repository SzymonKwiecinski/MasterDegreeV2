import pulp
import json

# Data provided in JSON format
data = json.loads('{"demand": [10.0, 20.0, 10.0], "max_regular_amount": 5.0, "cost_regular": 10.0, "cost_overtime": 12.0, "store_cost": 1.0}')

# Parameters
N = len(data['demand'])
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Create the LP problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(N)]

# Objective function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inventory[n] for n in range(N))

# Constraints
# Demand constraints
for n in range(N):
    if n == 0:
        inventory_prev = 0
    else:
        inventory_prev = inventory[n-1]

    problem += reg_quant[n] + over_quant[n] + inventory_prev - inventory[n] == demand[n]

# Regular production capacity constraint
for n in range(N):
    problem += reg_quant[n] <= max_regular_amount

# Solve the problem
problem.solve()

# Output results
reg_quant_values = [reg_quant[n].varValue for n in range(N)]
over_quant_values = [over_quant[n].varValue for n in range(N)]
print(f'Regular Quantities: {reg_quant_values}')
print(f'Overtime Quantities: {over_quant_values}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
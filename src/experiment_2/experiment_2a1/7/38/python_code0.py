import pulp
import json

# Input data
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}

# Number of months
N = len(data['demand'])

# Create the LP problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(N + 1)]

# Objective function
problem += (
    pulp.lpSum(data['cost_regular'] * reg_quant[n] for n in range(N)) +
    pulp.lpSum(data['cost_overtime'] * over_quant[n] for n in range(N)) +
    pulp.lpSum(data['store_cost'] * inventory[n] for n in range(1, N + 1))
)

# Constraints
for n in range(N):
    if n == 0:
        problem += (reg_quant[n] + over_quant[n] == data['demand'][n] + inventory[n], f'Demand_Constraint_{n}')
    else:
        problem += (reg_quant[n] + over_quant[n] + inventory[n] == data['demand'][n] + inventory[n-1], f'Demand_Constraint_{n}')
    
    problem += (reg_quant[n] <= data['max_regular_amount'], f'Max_Regular_Production_{n}')

# Inventory balance
for n in range(1, N + 1):
    problem += (inventory[n] == inventory[n - 1] + reg_quant[n - 1] + over_quant[n - 1] - data['demand'][n - 1], f'Inventory_Balance_{n}')

# Solve the problem
problem.solve()

# Output results
reg_quant_result = [pulp.value(reg_quant[n]) for n in range(N)]
over_quant_result = [pulp.value(over_quant[n]) for n in range(N)]

print(json.dumps({"reg_quant": reg_quant_result, "over_quant": over_quant_result}))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
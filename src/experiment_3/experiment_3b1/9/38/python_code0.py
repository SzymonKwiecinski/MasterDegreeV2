import pulp

# Data from the provided JSON format
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

# Define the problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Number of months
N = len(data['demand'])

# Decision Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(N)]

# Objective Function
problem += pulp.lpSum([
    data['cost_regular'] * reg_quant[n] +
    data['cost_overtime'] * over_quant[n] +
    data['store_cost'] * inventory[n] for n in range(N)
]), "Total_Cost"

# Constraints
for n in range(N):
    # Demand fulfillment
    if n == 0:
        problem += (reg_quant[n] + over_quant[n] >= data['demand'][n]), f"Demand_Fulfillment_{n+1}"
    else:
        problem += (reg_quant[n] + over_quant[n] + inventory[n-1] >= data['demand'][n]), f"Demand_Fulfillment_{n+1}"

    # Regular production capacity
    problem += (reg_quant[n] <= data['max_regular_amount']), f"Regular_Production_Capacity_{n+1}"

    # Inventory balance
    if n > 0:
        problem += (inventory[n] == inventory[n-1] + reg_quant[n] + over_quant[n] - data['demand'][n]), f"Inventory_Balance_{n+1}"
    else:
        problem += (inventory[n] == reg_quant[n] + over_quant[n] - data['demand'][n]), f"Inventory_Balance_{n+1}"

# Solve the problem
problem.solve()

# Output results
reg_quant_values = [pulp.value(var) for var in reg_quant]
over_quant_values = [pulp.value(var) for var in over_quant]

print(f'Regular Production Quantities: {reg_quant_values}')
print(f'Overtime Production Quantities: {over_quant_values}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
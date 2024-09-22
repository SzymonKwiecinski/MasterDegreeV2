import pulp

# Data
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

N = len(data['demand'])

# Create a Linear Programming problem
problem = pulp.LpProblem("ProductionScheduling", pulp.LpMinimize)

# Define decision variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(N)]

# Objective function
problem += pulp.lpSum(data['cost_regular'] * reg_quant[n] + 
                       data['cost_overtime'] * over_quant[n] + 
                       data['store_cost'] * inventory[n] for n in range(N))

# Demand satisfaction constraints
for n in range(N):
    if n == 0:
        problem += reg_quant[n] + over_quant[n] >= data['demand'][n], f'Demand_Satisfaction_{n}'
    else:
        problem += reg_quant[n] + over_quant[n] + inventory[n-1] >= data['demand'][n], f'Demand_Satisfaction_{n}'

# Regular production capacity constraints
for n in range(N):
    problem += reg_quant[n] <= data['max_regular_amount'], f'Regular_Production_Capacity_{n}'

# Inventory balance constraints
for n in range(N):
    if n == 0:
        problem += inventory[n] == reg_quant[n] + over_quant[n] - data['demand'][n], f'Inventory_Balance_{n}'
    else:
        problem += inventory[n] == inventory[n-1] + reg_quant[n] + over_quant[n] - data['demand'][n], f'Inventory_Balance_{n}'

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
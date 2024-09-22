import pulp

# Data
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

# Problem
num_months = len(data['demand'])
problem = pulp.LpProblem("Production_Planning", pulp.LpMinimize)

# Decision Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0, cat='Continuous') for n in range(num_months)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0, cat='Continuous') for n in range(num_months)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0, cat='Continuous') for n in range(num_months)]

# Objective Function
problem += pulp.lpSum([data['cost_regular'] * reg_quant[n] + 
                       data['cost_overtime'] * over_quant[n] + 
                       data['store_cost'] * inventory[n] for n in range(num_months)])

# Constraints
for n in range(num_months):
    if n == 0:
        # Initial Inventory considered as 0
        initial_inventory = 0
    else:
        initial_inventory = inventory[n - 1]

    # Demand satisfaction constraint
    problem += reg_quant[n] + over_quant[n] + initial_inventory >= data['demand'][n]
    # Regular production capacity constraint
    problem += reg_quant[n] <= data['max_regular_amount']
    # Inventory balance constraint
    problem += inventory[n] == initial_inventory + reg_quant[n] + over_quant[n] - data['demand'][n]

# Solve
problem.solve()

# Print Objective Value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
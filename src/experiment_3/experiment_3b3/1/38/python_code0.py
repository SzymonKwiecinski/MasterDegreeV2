import pulp

# Data from JSON
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

# Constants
N = len(data['demand'])
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Problem
problem = pulp.LpProblem("Production_Scheduling_Problem", pulp.LpMinimize)

# Decision Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(1, N+1)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(1, N+1)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(1, N+1)]

# Objective Function
problem += pulp.lpSum(cost_regular * reg_quant[n] + 
                      cost_overtime * over_quant[n] + 
                      store_cost * inventory[n] for n in range(N))

# Constraints
# Demand satisfaction constraints
for n in range(N):
    problem += (inventory[n] + reg_quant[n] + over_quant[n] >= demand[n], f'Demand_Satisfaction_{n+1}')

# Production capacity constraints
for n in range(N):
    problem += (reg_quant[n] <= max_regular_amount, f'Regular_Capacity_{n+1}')

# Inventory balance constraints
for n in range(1, N):
    problem += (inventory[n] == inventory[n-1] + reg_quant[n] + over_quant[n] - demand[n],
                f'Inventory_Balance_{n+1}')

# Initial inventory balance
problem += (inventory[0] == 0 + reg_quant[0] + over_quant[0] - demand[0], 'Initial_Inventory_Balance')

# Solve the problem
problem.solve()

# Objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
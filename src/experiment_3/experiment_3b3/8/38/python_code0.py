import pulp

# Define data from the JSON structure
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

# Initialize the problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Number of months
N = len(data['demand'])

# Decision Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(N)]

# Objective Function
problem += pulp.lpSum(data['cost_regular'] * reg_quant[n] +
                      data['cost_overtime'] * over_quant[n] +
                      data['store_cost'] * inventory[n] for n in range(N))

# Constraints

# Initial Inventory
initial_inventory = 0

# Demand Satisfaction and Inventory Balance
for n in range(N):
    if n == 0:
        problem += initial_inventory + reg_quant[n] + over_quant[n] >= data['demand'][n], f'demand_satisfaction_{n}'
        problem += inventory[n] == initial_inventory + reg_quant[n] + over_quant[n] - data['demand'][n], f'inventory_balance_{n}'
    else:
        problem += inventory[n-1] + reg_quant[n] + over_quant[n] >= data['demand'][n], f'demand_satisfaction_{n}'
        problem += inventory[n] == inventory[n-1] + reg_quant[n] + over_quant[n] - data['demand'][n], f'inventory_balance_{n}'

# Regular Production Capacity
for n in range(N):
    problem += reg_quant[n] <= data['max_regular_amount'], f'regular_capacity_{n}'

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
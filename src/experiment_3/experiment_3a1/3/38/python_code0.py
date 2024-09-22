import pulp

# Data from the provided JSON
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

# Create a linear programming problem
problem = pulp.LpProblem("ProductionScheduling", pulp.LpMinimize)

# Define variables
N = len(data['demand'])
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(N)]

# Objective function
problem += pulp.lpSum(
    data['cost_regular'] * reg_quant[n] + 
    data['cost_overtime'] * over_quant[n] + 
    data['store_cost'] * inventory[n] 
    for n in range(N)
)

# Constraints
for n in range(N):
    # Demand Satisfaction
    if n == 0:
        problem += reg_quant[n] + over_quant[n] >= data['demand'][n]
    else:
        problem += reg_quant[n] + over_quant[n] + inventory[n-1] >= data['demand'][n]

    # Regular Production Limit
    problem += reg_quant[n] <= data['max_regular_amount']

    # Inventory Balance
    if n == 0:
        problem += inventory[n] == reg_quant[n] + over_quant[n] - data['demand'][n]
    else:
        problem += inventory[n] == inventory[n-1] + reg_quant[n] + over_quant[n] - data['demand'][n]

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
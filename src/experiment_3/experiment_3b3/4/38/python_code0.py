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

# Problem
problem = pulp.LpProblem("Production_Schedule", pulp.LpMinimize)

# Decision Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(1, N+1)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(1, N+1)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(N+1)]

# Initial Inventory Constraint
problem += inventory[0] == 0

# Objective Function
problem += pulp.lpSum(
    data['cost_regular'] * reg_quant[n] + 
    data['cost_overtime'] * over_quant[n] + 
    data['store_cost'] * inventory[n+1]
    for n in range(N)
)

# Constraints
for n in range(N):
    # Demand Satisfaction
    problem += (reg_quant[n] + over_quant[n] + inventory[n] - inventory[n+1] == data['demand'][n])
    # Regular Production Limit
    problem += (reg_quant[n] <= data['max_regular_amount'])

# Solve
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Output the decision variables
reg_quant_values = [pulp.value(reg_quant[n]) for n in range(N)]
over_quant_values = [pulp.value(over_quant[n]) for n in range(N)]

print(f'Regular Quantities: {reg_quant_values}')
print(f'Overtime Quantities: {over_quant_values}')
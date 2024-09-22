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

# Create a linear programming problem
problem = pulp.LpProblem("Minimize_Production_and_Storage_Costs", pulp.LpMinimize)

# Decision Variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]
store = [pulp.LpVariable(f'store_{n}', lowBound=0) for n in range(N)]

# Objective Function
problem += pulp.lpSum([
    data['cost_regular'] * reg_quant[n] +
    data['cost_overtime'] * over_quant[n] +
    data['store_cost'] * store[n]
    for n in range(N)
])

# Constraints
# Regular production limit
for n in range(N):
    problem += reg_quant[n] <= data['max_regular_amount']

# Inventory and demand balance
for n in range(N):
    if n == 0:
        problem += reg_quant[n] + over_quant[n] == data['demand'][n] + store[n]
    else:
        problem += reg_quant[n] + over_quant[n] + store[n-1] == data['demand'][n] + store[n]

# Initial inventory constraint
problem += store[0] == 0

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
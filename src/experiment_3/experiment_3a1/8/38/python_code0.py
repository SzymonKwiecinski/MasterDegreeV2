import pulp

# Given data
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

# Parameters
N = len(data['demand'])
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Create a linear programming problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0) for n in range(N)]  # Regular production
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0) for n in range(N)]  # Overtime production
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(N)]  # Inventory

# Objective Function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inventory[n] for n in range(N))

# Constraints
for n in range(N):
    # Production limits
    problem += reg_quant[n] <= max_regular_amount

    # Inventory balance
    if n == 0:
        problem += inventory[n] == reg_quant[n] + over_quant[n] - demand[n]  # Initial inventory is 0
    else:
        problem += inventory[n] == inventory[n-1] + reg_quant[n] + over_quant[n] - demand[n]

# Non-negativity constraints are implicitly handled by setting lowBound=0 for decision variables

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
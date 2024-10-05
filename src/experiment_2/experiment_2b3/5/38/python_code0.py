import pulp

# Load data
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}
demands = data['demand']
max_regular = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
months = len(demands)

# Define LP problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Define decision variables
reg_prod = [pulp.LpVariable(f'reg_prod_{i}', lowBound=0, upBound=max_regular, cat='Continuous') for i in range(months)]
over_prod = [pulp.LpVariable(f'over_prod_{i}', lowBound=0, cat='Continuous') for i in range(months)]
inventory = [pulp.LpVariable(f'inventory_{i}', lowBound=0, cat='Continuous') for i in range(months + 1)]

# Initial inventory is zero
problem += inventory[0] == 0

# Add demand satisfaction constraints
for i in range(months):
    if i == 0:
        problem += reg_prod[i] + over_prod[i] == demands[i] + inventory[i+1]
    else:
        problem += reg_prod[i] + over_prod[i] + inventory[i] == demands[i] + inventory[i+1]

# Define the objective function: minimize total cost
total_cost = (
    pulp.lpSum(cost_regular * reg_prod[i] for i in range(months)) +
    pulp.lpSum(cost_overtime * over_prod[i] for i in range(months)) +
    pulp.lpSum(store_cost * inventory[i+1] for i in range(months))
)

problem += total_cost

# Solve the problem
problem.solve()

# Prepare output
reg_quant = [pulp.value(reg_prod[i]) for i in range(months)]
over_quant = [pulp.value(over_prod[i]) for i in range(months)]

output = {
    "reg_quant": reg_quant,
    "over_quant": over_quant
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
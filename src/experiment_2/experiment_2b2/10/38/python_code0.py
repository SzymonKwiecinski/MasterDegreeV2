import pulp

# Data from json
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

# Parameters
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
N = len(demand)

# LP problem
problem = pulp.LpProblem("Production_Schedule", pulp.LpMinimize)

# Decision variables
regular_production = [pulp.LpVariable(f'regular_prod_{n}', lowBound=0) for n in range(N)]
overtime_production = [pulp.LpVariable(f'overtime_prod_{n}', lowBound=0) for n in range(N)]
inventory = [pulp.LpVariable(f'inventory_{n}', lowBound=0) for n in range(N+1)]

# Objective function
production_cost = (
    pulp.lpSum(cost_regular * regular_production[n] for n in range(N)) +
    pulp.lpSum(cost_overtime * overtime_production[n] for n in range(N)) +
    pulp.lpSum(store_cost * inventory[n+1] for n in range(N))
)

problem += production_cost, "Total_Cost"

# Constraints
for n in range(N):
    # Demand constraint
    problem += (regular_production[n] + overtime_production[n] + inventory[n] == demand[n] + inventory[n+1]), f"Demand_Constraint_{n}"
    # Maximum regular production constraint
    problem += regular_production[n] <= max_regular_amount, f"Max_Regular_Production_{n}"

# Initial inventory is zero
problem += inventory[0] == 0, "Initial_Inventory"

# Solve the problem
problem.solve()

# Output
output = {
    "reg_quant": [pulp.value(regular_production[n]) for n in range(N)],
    "over_quant": [pulp.value(overtime_production[n]) for n in range(N)]
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
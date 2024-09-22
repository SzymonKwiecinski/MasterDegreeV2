import pulp

# Data input
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

# Extract data
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Number of months
n = len(demand)

# Initialize the problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision variables
reg_quant = pulp.LpVariable.dicts("regular_production", range(n), 0, max_regular_amount, cat='Continuous')
over_quant = pulp.LpVariable.dicts("overtime_production", range(n), 0, None, cat='Continuous')
inventory = pulp.LpVariable.dicts("inventory", range(n+1), 0, None, cat='Continuous')

# Objective function
total_cost = (
    pulp.lpSum(cost_regular * reg_quant[i] for i in range(n)) +
    pulp.lpSum(cost_overtime * over_quant[i] for i in range(n)) +
    pulp.lpSum(store_cost * inventory[i] for i in range(1, n+1))
)
problem += total_cost

# Constraints
problem += (inventory[0] == 0, "Initial_inventory")

for i in range(n):
    # Satisfy demand
    problem += (reg_quant[i] + over_quant[i] + inventory[i] == demand[i] + inventory[i+1], f"Demand_satisfaction_month_{i}")

# Solve the problem
problem.solve()

# Collect results
results = {
    "reg_quant": [pulp.value(reg_quant[i]) for i in range(n)],
    "over_quant": [pulp.value(over_quant[i]) for i in range(n)]
}

print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
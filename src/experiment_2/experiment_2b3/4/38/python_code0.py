import pulp

# Data
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}
demands = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
n_periods = len(demands)

# Problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision Variables
reg_production = [pulp.LpVariable(f"reg_prod_{n}", lowBound=0) for n in range(n_periods)]
overtime_production = [pulp.LpVariable(f"ovt_prod_{n}", lowBound=0) for n in range(n_periods)]
inventory = [pulp.LpVariable(f"inventory_{n}", lowBound=0) for n in range(n_periods)]

# Objective function
problem += pulp.lpSum(
    cost_regular * reg_production[n] + 
    cost_overtime * overtime_production[n] + 
    store_cost * inventory[n] for n in range(n_periods)
)

# Constraints
for n in range(n_periods):
    problem += reg_production[n] <= max_regular_amount, f"Max_Regular_Production_{n}"
    
    if n == 0:
        previous_inventory = 0
    else:
        previous_inventory = inventory[n-1]

    problem += reg_production[n] + overtime_production[n] + previous_inventory == demands[n] + inventory[n], f"Demand_Satisfaction_{n}"

# Solve
problem.solve()

# Results
reg_quant = [pulp.value(reg_production[n]) for n in range(n_periods)]
over_quant = [pulp.value(overtime_production[n]) for n in range(n_periods)]

output = {
    "reg_quant": reg_quant,
    "over_quant": over_quant
}

print(f' {output}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp

# Parse the data
data = {'demand': [10.0, 20.0, 10.0], 'max_regular_amount': 5.0, 'cost_regular': 10.0, 'cost_overtime': 12.0, 'store_cost': 1.0}

demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']
N = len(demand)

# Define the problem
problem = pulp.LpProblem("Production_Schedule", pulp.LpMinimize)

# Decision variables
reg_quant = [pulp.LpVariable(f'reg_quant_{n}', lowBound=0, cat='Continuous') for n in range(N)]
over_quant = [pulp.LpVariable(f'over_quant_{n}', lowBound=0, cat='Continuous') for n in range(N)]
stored_units = [pulp.LpVariable(f'stored_units_{n}', lowBound=0, cat='Continuous') for n in range(N)]

# Objective function
problem += (pulp.lpSum([cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * stored_units[n] for n in range(N)]), "Total Cost")

# Constraints
for n in range(N):
    # Demand satisfaction
    if n == 0:
        problem += (reg_quant[n] + over_quant[n] == demand[n] + stored_units[n], f"Demand_Constraint_{n}")
    else:
        problem += (reg_quant[n] + over_quant[n] + stored_units[n-1] == demand[n] + stored_units[n], f"Demand_Constraint_{n}")

    # Regular production limit
    problem += (reg_quant[n] <= max_regular_amount, f"Regular_Production_Limit_{n}")

# Solve the problem
problem.solve()

# Output the results
results = {
    "reg_quant": [reg_quant[n].varValue for n in range(N)],
    "over_quant": [over_quant[n].varValue for n in range(N)]
}

print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
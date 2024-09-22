import pulp

# Data from the provided JSON format
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

N = len(data['demand'])  # Number of months
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Create the linear programming problem
problem = pulp.LpProblem("Production_Cost_Minimization", pulp.LpMinimize)

# Define decision variables
reg_quant = pulp.LpVariable.dicts("reg_quant", range(N), lowBound=0)
over_quant = pulp.LpVariable.dicts("over_quant", range(N), lowBound=0)
inventory = pulp.LpVariable.dicts("inventory", range(N), lowBound=0)

# Objective function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inventory[n] for n in range(N))

# Constraints

# Demand satisfaction and inventory balance
for n in range(N):
    if n == 0:
        problem += reg_quant[n] + over_quant[n] >= demand[n], f"Demand_Satisfaction_{n}"
        problem += inventory[n] == reg_quant[n] + over_quant[n] - demand[n], f"Inventory_Balance_{n}"
    else:
        problem += reg_quant[n] + over_quant[n] + inventory[n-1] >= demand[n], f"Demand_Satisfaction_{n}"
        problem += inventory[n] == inventory[n-1] + reg_quant[n] + over_quant[n] - demand[n], f"Inventory_Balance_{n}"
    
    # Regular production limits
    problem += reg_quant[n] <= max_regular_amount, f"Regular_Production_Limit_{n}"

# Solve the problem
problem.solve()

# Output the results
reg_quant_values = [reg_quant[n].varValue for n in range(N)]
over_quant_values = [over_quant[n].varValue for n in range(N)]

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Regular production quantities: {reg_quant_values}')
print(f'Overtime production quantities: {over_quant_values}')
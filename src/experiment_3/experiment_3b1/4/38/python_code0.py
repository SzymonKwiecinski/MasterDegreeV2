import pulp

# Data from JSON input
data = {
    'demand': [10.0, 20.0, 10.0],
    'max_regular_amount': 5.0,
    'cost_regular': 10.0,
    'cost_overtime': 12.0,
    'store_cost': 1.0
}

N = len(data['demand'])
demand = data['demand']
max_regular_amount = data['max_regular_amount']
cost_regular = data['cost_regular']
cost_overtime = data['cost_overtime']
store_cost = data['store_cost']

# Create the linear programming problem
problem = pulp.LpProblem("Production_Scheduling", pulp.LpMinimize)

# Decision Variables
reg_quant = pulp.LpVariable.dicts("RegQuant", range(N), lowBound=0, upBound=max_regular_amount)
over_quant = pulp.LpVariable.dicts("OverQuant", range(N), lowBound=0)
inventory = pulp.LpVariable.dicts("Inventory", range(N + 1), lowBound=0)

# Objective Function
problem += pulp.lpSum(cost_regular * reg_quant[n] + cost_overtime * over_quant[n] + store_cost * inventory[n] for n in range(N))

# Constraints
# Initial inventory
problem += (inventory[0] == 0)

# Monthly constraints
for n in range(N):
    if n == 0:
        problem += (reg_quant[n] + over_quant[n] - inventory[n] == demand[n])
    else:
        problem += (reg_quant[n] + over_quant[n] + inventory[n-1] - inventory[n] == demand[n])
    
    # Maximum regular production constraint
    problem += (reg_quant[n] <= max_regular_amount)
    
    # Non-negativity of inventory
    problem += (inventory[n] >= 0)

# Solve the problem
problem.solve()

# Output results
reg_quant_result = [reg_quant[n].varValue for n in range(N)]
over_quant_result = [over_quant[n].varValue for n in range(N)]

print(f'Regular Production Quantities: {reg_quant_result}')
print(f'Overtime Production Quantities: {over_quant_result}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
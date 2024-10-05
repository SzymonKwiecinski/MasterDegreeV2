import pulp

# Problem data
data = {
    'N': 2, 
    'AssemblyHour': [0.25, 0.3333], 
    'TestingHour': [0.125, 0.3333], 
    'MaterialCost': [1.2, 0.9], 
    'MaxAssembly': 10, 
    'MaxTesting': 70, 
    'Price': [9, 8], 
    'MaxOvertimeAssembly': 50, 
    'OvertimeAssemblyCost': 5, 
    'MaterialDiscount': 10, 
    'DiscountThreshold': 300
}

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
units_produced = [pulp.LpVariable(f'Units_Produced_{i}', lowBound=0, cat='Integer') for i in range(data['N'])]
overtime_assembly = pulp.LpVariable('Overtime_Assembly', lowBound=0, upBound=data['MaxOvertimeAssembly'], cat='Continuous')

# Constraints
# Assembly hour constraint
problem += (pulp.lpSum([data['AssemblyHour'][i] * units_produced[i] for i in range(data['N'])]) + overtime_assembly <= data['MaxAssembly'])

# Testing hour constraint
problem += (pulp.lpSum([data['TestingHour'][i] * units_produced[i] for i in range(data['N'])]) <= data['MaxTesting'])

# Objective function
total_revenue = pulp.lpSum([data['Price'][i] * units_produced[i] for i in range(data['N'])])
total_material_cost = pulp.lpSum([data['MaterialCost'][i] * units_produced[i] for i in range(data['N'])])

# Apply discount if total material cost is above threshold
if total_material_cost >= data['DiscountThreshold']:
    total_material_cost *= (1 - data['MaterialDiscount'] / 100)

total_overtime_cost = overtime_assembly * data['OvertimeAssemblyCost']
total_cost = total_material_cost + total_overtime_cost

daily_profit = total_revenue - total_cost

problem += daily_profit

# Solve the problem
problem.solve()

# Output results
output = {
    "dailyProfit": pulp.value(problem.objective),
    "unitsProduced": [pulp.value(units_produced[i]) for i in range(data['N'])],
    "overtimeAssembly": pulp.value(overtime_assembly),
    "materialBought": pulp.value(pulp.lpSum([data['MaterialCost'][i] * units_produced[i] for i in range(data['N'])]))
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
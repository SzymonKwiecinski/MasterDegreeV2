import pulp

# Data from the provided JSON format
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

# Create the Linear Program problem
problem = pulp.LpProblem("Daily_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
unitsProduced = [pulp.LpVariable(f'unitsProduced_{i}', lowBound=0) for i in range(data['N'])]
overtimeAssembly = pulp.LpVariable('overtimeAssembly', lowBound=0)
materialBought = pulp.LpVariable('materialBought', lowBound=0)

# Objective Function
material_costs = pulp.lpSum(data['MaterialCost'][i] * unitsProduced[i] for i in range(data['N']))
sales_revenue = pulp.lpSum(data['Price'][i] * unitsProduced[i] for i in range(data['N']))
discount = pulp.lpSum(data['MaterialCost'][i] * unitsProduced[i] for i in range(data['N'])) * (data['MaterialDiscount'] / 100)

# Apply discount condition
total_material_cost = material_costs
apply_discount = total_material_cost >= data['DiscountThreshold']
discount_value = pulp.lpIf(apply_discount, discount, 0)

problem += sales_revenue - (material_costs + overtimeAssembly * data['OvertimeAssemblyCost'] - discount_value), "Total_Profit"

# Constraints
# Assembly labor constraint
problem += pulp.lpSum(data['AssemblyHour'][i] * unitsProduced[i] for i in range(data['N'])) + overtimeAssembly <= data['MaxAssembly'] + data['MaxOvertimeAssembly'], "Assembly_Labor_Constraint"

# Testing labor constraint
problem += pulp.lpSum(data['TestingHour'][i] * unitsProduced[i] for i in range(data['N'])) <= data['MaxTesting'], "Testing_Labor_Constraint"

# Solve the problem
problem.solve()

# Output results
daily_profit = pulp.value(problem.objective)
units_produced = [pulp.value(u) for u in unitsProduced]
overtime_hours = pulp.value(overtimeAssembly)
material_bought = pulp.value(materialBought)

print(f' (Objective Value): <OBJ>{daily_profit}</OBJ>')
print(f'Units Produced: {units_produced}')
print(f'Overtime Assembly Hours: {overtime_hours}')
print(f'Material Bought: {material_bought}')
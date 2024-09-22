import pulp

# Problem data from JSON
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
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

# Decision variables
units_produced = [pulp.LpVariable(f'Units_Produced_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]
overtime_assembly = pulp.LpVariable('Overtime_Assembly', lowBound=0, upBound=data['MaxOvertimeAssembly'], cat='Continuous')

# Objective function: Maximize revenue - cost
revenue = pulp.lpSum(data['Price'][i] * units_produced[i] for i in range(data['N']))
material_cost = pulp.lpSum(data['MaterialCost'][i] * units_produced[i] for i in range(data['N']))
assembly_cost = overtime_assembly * data['OvertimeAssemblyCost']

# Apply material discount
discounted_material_cost = pulp.LpVariable('Discounted_Material_Cost', lowBound=0, cat='Continuous')
problem += discounted_material_cost == material_cost, "MaterialCostAdjustment"
problem += discounted_material_cost >= ((100 - data['MaterialDiscount']) / 100) * material_cost, "MaterialDiscountCondition"
problem += discounted_material_cost >= material_cost - pulp.lpSum([pulp.lpSum(data['MaterialCost'][i] * units_produced[i] for i in range(data['N'])) * data['MaterialDiscount'] / 100]), "DiscountThresholdCondition" 

# Profit = Revenue - Costs
profit = revenue - discounted_material_cost - assembly_cost
problem += profit

# Constraints
# Assembly hours
problem += pulp.lpSum(data['AssemblyHour'][i] * units_produced[i] for i in range(data['N'])) <= data['MaxAssembly'] + overtime_assembly, "MaxAssembly"

# Testing hours
problem += pulp.lpSum(data['TestingHour'][i] * units_produced[i] for i in range(data['N'])) <= data['MaxTesting'], "MaxTesting"

# Solve the problem
problem.solve()

# Collect results
units_produced_values = [pulp.value(units_produced[i]) for i in range(data['N'])]
overtime_assembly_value = pulp.value(overtime_assembly)
material_bought_value = material_cost.value()
daily_profit_value = pulp.value(profit)

# Print the results
output = {
    "dailyProfit": daily_profit_value,
    "unitsProduced": units_produced_values,
    "overtimeAssembly": overtime_assembly_value,
    "materialBought": material_bought_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
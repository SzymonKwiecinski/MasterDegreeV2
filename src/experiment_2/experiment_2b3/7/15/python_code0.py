import pulp

# Extract data from the JSON format
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

# Define the problem
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

# Decision variables
unitsProduced = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Integer') for i in range(data['N'])]
overtimeAssembly = pulp.LpVariable("overtime_assembly", lowBound=0, upBound=data['MaxOvertimeAssembly'], cat='Continuous')
materialBought = pulp.LpVariable("material_bought", lowBound=0)

# Objective function components
total_revenue = pulp.lpSum([data['Price'][i] * unitsProduced[i] for i in range(data['N'])])
total_material_cost = pulp.lpSum([data['MaterialCost'][i] * unitsProduced[i] for i in range(data['N'])])

# Apply discount if the threshold is reached
discounted_material_cost = total_material_cost * (1 - data['MaterialDiscount'] / 100)
material_cost = pulp.lpSum([discounted_material_cost if total_material_cost > data['DiscountThreshold'] else total_material_cost])

# Cost components
assembly_cost = overtimeAssembly * data['OvertimeAssemblyCost']

# Profit calculation
daily_profit = total_revenue - (material_cost + assembly_cost)

# Objective function
problem += daily_profit

# Constraints
# Assembly labor constraints
problem += pulp.lpSum([data['AssemblyHour'][i] * unitsProduced[i] for i in range(data['N'])]) <= data['MaxAssembly'] + overtimeAssembly, "AssemblyLabor"

# Testing labor constraints
problem += pulp.lpSum([data['TestingHour'][i] * unitsProduced[i] for i in range(data['N'])]) <= data['MaxTesting'], "TestingLabor"

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "dailyProfit": pulp.value(daily_profit),
    "unitsProduced": [pulp.value(units) for units in unitsProduced],
    "overtimeAssembly": pulp.value(overtimeAssembly),
    "materialBought": pulp.value(total_material_cost)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
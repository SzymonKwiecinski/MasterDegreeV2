import pulp

# Parse the input data
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
units_produced = [pulp.LpVariable(f"unitsProduced_{i}", lowBound=0, cat='Integer') for i in range(data['N'])]
overtime_assembly = pulp.LpVariable("overtimeAssembly", lowBound=0, cat='Continuous')

# Constraints
# Assembly time constraint
problem += pulp.lpSum([units_produced[i] * data['AssemblyHour'][i] for i in range(data['N'])]) <= data['MaxAssembly'] + overtime_assembly

# Testing time constraint
problem += pulp.lpSum([units_produced[i] * data['TestingHour'][i] for i in range(data['N'])]) <= data['MaxTesting']

# Overtime assembly constraint
problem += overtime_assembly <= data['MaxOvertimeAssembly']

# Objective function
# Revenue
revenue = pulp.lpSum([units_produced[i] * data['Price'][i] for i in range(data['N'])])

# Material cost
material_cost = pulp.lpSum([units_produced[i] * data['MaterialCost'][i] for i in range(data['N'])])

# Apply material discount if applicable
material_cost_after_discount = pulp.LpVariable("materialCostAfterDiscount", lowBound=0, cat='Continuous')
problem += material_cost_after_discount == material_cost * (1 - data['MaterialDiscount'] / 100), "MaterialCostAfterDiscount"
problem += material_cost_after_discount >= data['DiscountThreshold'], "DiscountThreshold"

# Overtime cost
overtime_cost = overtime_assembly * data['OvertimeAssemblyCost']

# Total cost
total_cost = material_cost - material_cost_after_discount + overtime_cost

# Profit
daily_profit = revenue - total_cost

# Set the objective
problem += daily_profit

# Solve the problem
problem.solve()

# Output results
output = {
    "dailyProfit": pulp.value(daily_profit),
    "unitsProduced": [pulp.value(units_produced[i]) for i in range(data['N'])],
    "overtimeAssembly": pulp.value(overtime_assembly),
    "materialBought": pulp.value(material_cost)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
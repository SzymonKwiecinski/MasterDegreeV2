import pulp

# Data from the JSON input
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

# Unpacking data
N = data['N']
assembly_hour = data['AssemblyHour']
testing_hour = data['TestingHour']
material_cost = data['MaterialCost']
max_assembly = data['MaxAssembly']
max_testing = data['MaxTesting']
price = data['Price']
max_overtime_assembly = data['MaxOvertimeAssembly']
overtime_assembly_cost = data['OvertimeAssemblyCost']
material_discount = data['MaterialDiscount']
discount_threshold = data['DiscountThreshold']

# Problem
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

# Decision variables
units_produced = [pulp.LpVariable(f'units_prod_{i}', lowBound=0, cat='Integer') for i in range(N)]
overtime_assembly = pulp.LpVariable('overtime_assembly', lowBound=0, cat='Continuous')

# Constraints

# Constraint: Max Assembly hours including overtime
problem += pulp.lpSum([assembly_hour[i] * units_produced[i] for i in range(N)]) <= max_assembly + overtime_assembly

# Constraint: Max Testing hours
problem += pulp.lpSum([testing_hour[i] * units_produced[i] for i in range(N)]) <= max_testing

# Constraint: Overtime assembly hours must not exceed max overtime allowed
problem += overtime_assembly <= max_overtime_assembly

# Objective
revenue = pulp.lpSum([price[i] * units_produced[i] for i in range(N)])
material_usage = pulp.lpSum([material_cost[i] * units_produced[i] for i in range(N)])

# Apply discount if daily bill exceeds discount threshold
material_cost_discounted = pulp.lpSum([
    material_cost[i] * units_produced[i] * (1 - material_discount / 100) if material_usage > discount_threshold else material_cost[i] * units_produced[i]
    for i in range(N)
])

total_cost = material_cost_discounted + overtime_assembly_cost * overtime_assembly
profit = revenue - total_cost

problem += profit

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "dailyProfit": pulp.value(profit),
    "unitsProduced": [pulp.value(units_produced[i]) for i in range(N)],
    "overtimeAssembly": pulp.value(overtime_assembly),
    "materialBought": pulp.value(material_usage)
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
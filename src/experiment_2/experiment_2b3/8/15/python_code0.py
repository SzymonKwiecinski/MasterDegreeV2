import pulp

# Load data
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
    'DiscountThreshold': 300,
}

# Extract the required information from the data
N = data['N']
assembly_hours = data['AssemblyHour']
testing_hours = data['TestingHour']
material_costs = data['MaterialCost']
max_assembly = data['MaxAssembly']
max_testing = data['MaxTesting']
prices = data['Price']
max_overtime_assembly = data['MaxOvertimeAssembly']
overtime_assembly_cost = data['OvertimeAssemblyCost']
material_discount = data['MaterialDiscount']
discount_threshold = data['DiscountThreshold']

# Define the decision variables
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)
units_produced = [pulp.LpVariable(f'Units_{i}', lowBound=0, cat='Integer') for i in range(N)]
overtime_assembly = pulp.LpVariable('Overtime_Assembly', lowBound=0, upBound=max_overtime_assembly, cat='Continuous')

# Objective function (maximize profit)
revenue = pulp.lpSum([prices[i] * units_produced[i] for i in range(N)])
total_material_cost = pulp.lpSum([material_costs[i] * units_produced[i] for i in range(N)])
if total_material_cost > discount_threshold:
    total_material_cost *= (1 - material_discount / 100)
total_overtime_cost = overtime_assembly * overtime_assembly_cost

profit = revenue - total_material_cost - total_overtime_cost
problem += profit

# Constraints
# Assembly labor constraint
problem += pulp.lpSum([assembly_hours[i] * units_produced[i] for i in range(N)]) + overtime_assembly <= max_assembly + max_overtime_assembly
# Testing labor constraint
problem += pulp.lpSum([testing_hours[i] * units_produced[i] for i in range(N)]) <= max_testing

# Solve the problem
problem.solve()

# Output results
units_produced_values = [pulp.value(units_produced[i]) for i in range(N)]
overtime_assembly_value = pulp.value(overtime_assembly)
material_bought_value = sum([material_costs[i] * units_produced_values[i] for i in range(N)])

output = {
    "dailyProfit": pulp.value(problem.objective),
    "unitsProduced": units_produced_values,
    "overtimeAssembly": overtime_assembly_value,
    "materialBought": material_bought_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp

# Parse the input data
data = {'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}

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

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
units_produced = [pulp.LpVariable(f'UnitsProduced_{i+1}', lowBound=0, cat='Integer') for i in range(N)]
overtime_assembly = pulp.LpVariable('OvertimeAssembly', lowBound=0, cat='Continuous')
material_bought = pulp.LpVariable('MaterialBought', lowBound=0, cat='Continuous')

# Total revenue
total_revenue = pulp.lpSum([price[i] * units_produced[i] for i in range(N)])

# Total cost
total_material_cost = pulp.lpSum([material_cost[i] * units_produced[i] for i in range(N)])
discounted_material_cost = total_material_cost * (1 - material_discount / 100) if total_material_cost > discount_threshold else total_material_cost
total_overtime_cost = overtime_assembly * overtime_assembly_cost
total_cost = discounted_material_cost + total_overtime_cost

# Objective function: Maximize profit
problem += total_revenue - total_cost

# Constraints
problem += pulp.lpSum([assembly_hour[i] * units_produced[i] for i in range(N)]) <= max_assembly + overtime_assembly, "AssemblyHoursConstraint"
problem += pulp.lpSum([testing_hour[i] * units_produced[i] for i in range(N)]) <= max_testing, "TestingHoursConstraint"
problem += overtime_assembly <= max_overtime_assembly, "OvertimeAssemblyConstraint"
problem += material_bought == total_material_cost, "MaterialBoughtConstraint"

# Solve the problem
problem.solve()

# Retrieve the results
result = {
    "dailyProfit": pulp.value(problem.objective),
    "unitsProduced": [pulp.value(units_produced[i]) for i in range(N)],
    "overtimeAssembly": pulp.value(overtime_assembly),
    "materialBought": pulp.value(material_bought)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
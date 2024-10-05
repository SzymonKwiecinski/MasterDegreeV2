import pulp

data = {'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}

# Extract data
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

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
units_produced = [pulp.LpVariable(f'units_{i}', lowBound=0, cat='Integer') for i in range(N)]
overtime_assembly = pulp.LpVariable('overtime_assembly', lowBound=0, upBound=max_overtime_assembly, cat='Continuous')

# Objective function components
total_revenue = pulp.lpSum([prices[i] * units_produced[i] for i in range(N)])
total_material_cost = pulp.lpSum([material_costs[i] * units_produced[i] for i in range(N)])

# Create constraint for discount condition
discount_condition = total_material_cost - discount_threshold

# Define the total cost including the discount logic
total_cost = (
    pulp.lpSum([material_costs[i] * units_produced[i] for i in range(N)]) -
    (material_discount / 100) * pulp.lpMax(discount_condition, 0) + 
    overtime_assembly * overtime_assembly_cost
)

profit = total_revenue - total_cost

problem += profit

# Constraints
problem += pulp.lpSum([assembly_hours[i] * units_produced[i] for i in range(N)]) <= max_assembly + overtime_assembly, "Assembly_hours_constraint"
problem += pulp.lpSum([testing_hours[i] * units_produced[i] for i in range(N)]) <= max_testing, "Testing_hours_constraint"

# Solve the problem
problem.solve()

# Prepare output
daily_profit = pulp.value(problem.objective)
units_produced_values = [pulp.value(units_produced[i]) for i in range(N)]
overtime_assembly_value = pulp.value(overtime_assembly)
material_bought = pulp.value(total_material_cost)

output = {
    "dailyProfit": daily_profit,
    "unitsProduced": units_produced_values,
    "overtimeAssembly": overtime_assembly_value,
    "materialBought": material_bought
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp

# Define the problem data from the provided JSON data
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

# Unpack data for clarity
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

# Define the problem
problem = pulp.LpProblem("ProfitMaximization", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(N)]
overtime_assembly = pulp.LpVariable('overtimeAssembly', lowBound=0, cat='Continuous')

# Objective function components
total_revenue = pulp.lpSum(prices[i] * x[i] for i in range(N))
total_material_cost = pulp.lpSum(material_costs[i] * x[i] for i in range(N))
total_overtime_cost = overtime_assembly * overtime_assembly_cost

# Calculate discount
material_cost_expr = pulp.lpSum(material_costs[i] * x[i] for i in range(N))
discount = material_discount / 100 * material_cost_expr

# Create a constraint that forces the discount indicator to be a binary variable
discount_indicator = pulp.LpVariable('discount_indicator', cat='Binary')
problem += material_cost_expr - discount_threshold <= (1 - discount_indicator) * 1000000  # large number
problem += discount_threshold - material_cost_expr <= discount_indicator * 1000000  # large number

# Discount expression
discount_expr = discount_indicator * discount

# Objective Function: Maximize daily profit
problem += total_revenue - total_material_cost - total_overtime_cost - discount_expr

# Constraints
# Assembly labor constraint
problem += pulp.lpSum(assembly_hours[i] * x[i] for i in range(N)) + overtime_assembly <= max_assembly + max_overtime_assembly

# Testing labor constraint
problem += pulp.lpSum(testing_hours[i] * x[i] for i in range(N)) <= max_testing

# Solve the problem
problem.solve()

# Extracting the results
units_produced = [pulp.value(x[i]) for i in range(N)]
overtime_assembly_used = pulp.value(overtime_assembly)
material_bought = pulp.value(total_material_cost)

# Print the output
print("Daily Profit:", pulp.value(problem.objective))
print("Units Produced:", units_produced)
print("Overtime Assembly Used:", overtime_assembly_used)
print("Material Cost (Bought):", material_bought)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
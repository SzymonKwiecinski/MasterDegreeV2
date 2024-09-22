import pulp

# Data provided
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

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]
o = pulp.LpVariable('o', lowBound=0, cat='Continuous')

# Problem definition
problem = pulp.LpProblem('Daily_Profit_Maximization', pulp.LpMaximize)

# Objective function with conditional logic
material_costs = pulp.lpSum([data['MaterialCost'][i] * x[i] for i in range(data['N'])])
prices = pulp.lpSum([data['Price'][i] * x[i] for i in range(data['N'])])

# Create an indicator variable for the material discount
indicator_material_discount = pulp.LpVariable('indicator_material_discount', cat='Binary')

# Add constraints to handle the indicator variable
problem += material_costs <= data['DiscountThreshold'] + (1 - indicator_material_discount) * 1e6, "Discount Threshold Constraint"

discount_multiplier = 1 - (data['MaterialDiscount'] / 100) * indicator_material_discount

overtime_cost = data['OvertimeAssemblyCost'] * o
indicator_overtime = o > 0

total_cost = (material_costs + overtime_cost * indicator_overtime) * discount_multiplier
profit = prices - total_cost

problem += profit, "Objective: Maximize Daily Profit"

# Constraints
problem += pulp.lpSum([data['AssemblyHour'][i] * x[i] for i in range(data['N'])]) + o <= data['MaxAssembly'] + data['MaxOvertimeAssembly'], "Assembly Time Constraint"
problem += pulp.lpSum([data['TestingHour'][i] * x[i] for i in range(data['N'])]) <= data['MaxTesting'], "Testing Time Constraint"

# Solve the problem
problem.solve()

# Display results
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
for i in range(data['N']):
    print(f'Units produced of product {i+1}: {pulp.value(x[i])}')
print(f'Overtime assembly hours scheduled: {pulp.value(o)}')
print(f'Total cost of raw materials purchased: {pulp.value(material_costs)}')
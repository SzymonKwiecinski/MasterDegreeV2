import pulp

# Load data
data = {'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 
        'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 
        'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 
        'MaterialDiscount': 10, 'DiscountThreshold': 300}

# Create a linear programming problem
problem = pulp.LpProblem("Daily_Profit_Maximization", pulp.LpMaximize)

# Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]
h_overtime = pulp.LpVariable('h_overtime', lowBound=0, cat='Continuous')

# Objective Function
total_material_cost = sum(data['MaterialCost'][i] * x[i] for i in range(data['N']))
material_discount_value = (data['MaterialDiscount']/100) * pulp.lpSum([pulp.lpSum([data['MaterialCost'][i] * x[i] for i in range(data['N'])]) - data['DiscountThreshold']])
effective_material_cost = total_material_cost - material_discount_value
revenue = sum(data['Price'][i] * x[i] for i in range(data['N']))

problem += revenue - effective_material_cost - data['OvertimeAssemblyCost'] * h_overtime

# Constraints
# Assembly hours constraint
problem += sum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + h_overtime <= data['MaxAssembly'] + data['MaxOvertimeAssembly']

# Testing hours constraint
problem += sum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting']

# Solve the problem
problem.solve()

# Output Results
print(f'Daily Profit (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
for i in range(data['N']):
    print(f'Units produced of product {i+1}: {pulp.value(x[i])}')
print(f'Overtime Assembly Hours: {pulp.value(h_overtime)}')
material_cost_used = sum(data['MaterialCost'][i] * pulp.value(x[i]) for i in range(data['N']))
print(f'Material Bought: {material_cost_used}')
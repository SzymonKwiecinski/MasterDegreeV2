import pulp

# Extracting data from JSON format
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
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]
y = pulp.LpVariable('y', lowBound=0, cat='Continuous')
discount_applied = pulp.LpVariable('discount_applied', lowBound=0, cat='Continuous')

# Objective function
material_bought = pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N']))
problem += (
    pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))
    - (material_bought - discount_applied)
    - (y * data['OvertimeAssemblyCost'])
)

# Constraints
problem += (pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) <= data['MaxAssembly'] + y), "Assembly_Capacity"
problem += (pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting']), "Testing_Capacity"
problem += (y <= data['MaxOvertimeAssembly']), "Overtime_Capacity"

# Discount constraints
problem += (material_bought <= data['DiscountThreshold'] + (1 - discount_applied)), "No_Discount_Condition"
problem += (discount_applied == (data['MaterialDiscount'] * material_bought / 100)), "Discount_Applied"

# Solve the problem
problem.solve()

# Output results
daily_profit = pulp.value(problem.objective)
units_produced = [pulp.value(x[i]) for i in range(data['N'])]
overtime_assembly = pulp.value(y)
material_bought_value = sum(data['MaterialCost'][i] * units_produced[i] for i in range(data['N']))

print(f'Daily Profit: {daily_profit}')
print(f'Units Produced: {units_produced}')
print(f'Overtime Assembly: {overtime_assembly}')
print(f'Material Bought: {material_bought_value}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
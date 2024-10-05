import pulp

# Data from JSON
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

# Problem
problem = pulp.LpProblem("Production_Maximization", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]
overtimeAssembly = pulp.LpVariable('overtimeAssembly', lowBound=0, cat='Continuous')

# Discount calculation
total_material_cost = pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N']))
discount = pulp.LpVariable('discount', lowBound=0, cat='Continuous')

# Objective Function
profit = (
    pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) 
    - total_material_cost 
    + discount
    - overtimeAssembly * data['OvertimeAssemblyCost']
)
problem += profit

# Constraints
problem += (pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + overtimeAssembly <= data['MaxAssembly'] + data['MaxOvertimeAssembly']), 'Assembly_Labor_Constraint'
problem += (pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting']), 'Testing_Hours_Constraint'

# Material cost constraint for discount
problem += (
    discount <= data['MaterialDiscount'] / 100 * total_material_cost
), 'Discount_Constraint'
problem += (
    discount <= (total_material_cost - data['DiscountThreshold']) * 1000
), 'Discount_Threshold_Constraint'

# Solve
problem.solve()

# Outputs
unitsProduced = [pulp.value(x[i]) for i in range(data['N'])]
overtimeHours = pulp.value(overtimeAssembly)
totalMaterialBought = pulp.value(total_material_cost)

# Display Objective
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Other Outputs
print(f'Units Produced: {unitsProduced}')
print(f'Overtime Assembly Hours: {overtimeHours}')
print(f'Total Material Cost: {totalMaterialBought}')
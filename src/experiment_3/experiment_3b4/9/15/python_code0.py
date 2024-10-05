import pulp

# Parse JSON data
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

# Define the MILP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Define decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Integer') for i in range(data['N'])]
z = pulp.LpVariable('z', lowBound=0, cat='Integer')

# Define the effective material cost
effective_material_cost = sum(data['MaterialCost'][i] * x[i] for i in range(data['N']))

# Applying discount logic
discount_condition = effective_material_cost > data['DiscountThreshold']
effective_material_cost_with_discount = pulp.lpSum([
    (data['MaterialCost'][i] * x[i] * (1 - data['MaterialDiscount'] / 100)) for i in range(data['N'])
])

# Define the objective function
profit_without_discount = pulp.lpSum(data['Price'][i] * x[i] - data['MaterialCost'][i] * x[i] for i in range(data['N'])) - data['OvertimeAssemblyCost'] * z
profit_with_discount = pulp.lpSum(data['Price'][i] * x[i] - effective_material_cost_with_discount for i in range(data['N'])) - data['OvertimeAssemblyCost'] * z

# Add objective to problem: maximize profit
# Use conditional expression based on discount_condition
problem += discount_condition * profit_with_discount + (1 - discount_condition) * profit_without_discount

# Constraints
# Assembly hours
problem += pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) <= data['MaxAssembly'] + z

# Testing hours
problem += pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting']

# Overtime limit
problem += z <= data['MaxOvertimeAssembly']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp

# Data from the JSON format
data = {'N': 2, 
        'AssemblyHour': [0.25, 0.3333], 
        'TestingHour': [0.125, 0.3333], 
        'MaterialCost': [1.2, 0.9], 
        'MaxAssembly': 10, 
        'MaxTesting': 70, 
        'Price': [9, 8], 
        'MaxOvertimeAssembly': 50, 
        'OvertimeAssemblyCost': 5, 
        'MaterialDiscount': 10, 
        'DiscountThreshold': 300}

# Create a linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(data['N'])]
y = pulp.LpVariable('y', lowBound=0)

# Objective function
daily_profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) - \
    (pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N'])) - 
     (data['MaterialDiscount'] / 100) * pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N'])) 
     * pulp.lpIndicator(pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N'])) > data['DiscountThreshold'])) - \
    (data['OvertimeAssemblyCost'] * y)

problem += daily_profit

# Constraints
problem += pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + y <= data['MaxAssembly'] + data['MaxOvertimeAssembly']
problem += pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting']

# Solve the problem
problem.solve()

# Output results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
for i in range(data['N']):
    print(f'Units produced for product {i+1}: {pulp.value(x[i])}')
print(f'Overtime hours scheduled: {pulp.value(y)}')
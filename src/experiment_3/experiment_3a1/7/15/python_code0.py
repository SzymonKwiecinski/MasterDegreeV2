import pulp

# Data from JSON format
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
problem = pulp.LpProblem("MILP_Problem", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]
y = pulp.LpVariable('y', lowBound=0, cat='Continuous')

# Objective function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) - \
         (pulp.lpSum(data['MaterialCost'][i] * x[i] * (1 - data['MaterialDiscount'] / 100) for i in range(data['N'])) + data['OvertimeAssemblyCost'] * y)

problem += profit, "Total_Profit"

# Constraints
problem += (pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + y <= data['MaxAssembly'] + data['MaxOvertimeAssembly']), "Assembly_Labor_Constraint"
problem += (pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting']), "Testing_Labor_Constraint"
problem += (y <= data['MaxOvertimeAssembly']), "Overtime_Hours_Constraint"

# Solve the problem
problem.solve()

# Output
daily_profit = pulp.value(problem.objective)
units_produced = [pulp.value(x[i]) for i in range(data['N'])]
overtime_hours = pulp.value(y)
material_bought = sum(data['MaterialCost'][i] * x[i].varValue * (1 - data['MaterialDiscount'] / 100) for i in range(data['N']))

print(f' (Objective Value): <OBJ>{daily_profit}</OBJ>')
print(f'Units Produced: {units_produced}')
print(f'Overtime Assembly Hours: {overtime_hours}')
print(f'Material Bought: {material_bought}')
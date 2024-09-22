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

# Problem definition
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Integer') for i in range(data['N'])]
y = pulp.LpVariable('y', lowBound=0, cat='Integer')
z = pulp.LpVariable('z', cat='Binary')

# Objective function
profit = (
    pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) -
    pulp.lpSum(data['MaterialCost'][i] * x[i] * (1 - data['MaterialDiscount'] * z / 100) for i in range(data['N'])) -
    data['OvertimeAssemblyCost'] * y
)
problem += profit

# Constraints
problem += pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) <= data['MaxAssembly'] + y
problem += pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting']
problem += y <= data['MaxOvertimeAssembly']
problem += pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N'])) >= data['DiscountThreshold'] * z

# Solve the problem
problem.solve()

# Outputs
daily_profit = pulp.value(profit)
units_produced = [pulp.value(x[i]) for i in range(data['N'])]
overtime_assembly = pulp.value(y)
total_material_cost = pulp.lpSum(data['MaterialCost'][i] * units_produced[i] * (1 - data['MaterialDiscount'] * pulp.value(z) / 100) for i in range(data['N']))

print(f"Daily Profit: {daily_profit}")
print(f"Units Produced: {units_produced}")
print(f"Overtime Assembly Hours: {overtime_assembly}")
print(f"Total Material Cost: {total_material_cost}")
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
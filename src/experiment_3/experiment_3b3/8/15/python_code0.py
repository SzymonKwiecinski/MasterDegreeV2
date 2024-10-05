import pulp

# Data
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
problem = pulp.LpProblem("Daily_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]
overtimeAssembly = pulp.LpVariable('overtimeAssembly', lowBound=0, cat='Continuous')

# Objective Function
profit_without_discount = sum(data['Price'][i] * x[i] for i in range(data['N'])) - \
                          sum(data['MaterialCost'][i] * x[i] for i in range(data['N'])) - \
                          (data['OvertimeAssemblyCost'] * overtimeAssembly)
total_material_cost = sum(data['MaterialCost'][i] * x[i] for i in range(data['N']))

# Apply discount if total material cost is above threshold
if total_material_cost >= data['DiscountThreshold']:
    discount_factor = 1 - data['MaterialDiscount'] / 100
else:
    discount_factor = 1

discounted_material_cost = sum(data['MaterialCost'][i] * discount_factor * x[i] for i in range(data['N']))
discounted_profit = sum(data['Price'][i] * x[i] for i in range(data['N'])) - \
                    discounted_material_cost - \
                    (data['OvertimeAssemblyCost'] * overtimeAssembly)

problem += discounted_profit

# Constraints
problem += sum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + overtimeAssembly <= data['MaxAssembly'] + data['MaxOvertimeAssembly']
problem += sum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting']

# Solve
problem.solve()

# Objective Value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
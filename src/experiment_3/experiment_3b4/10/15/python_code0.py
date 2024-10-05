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

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i+1}', lowBound=0, cat='Integer') for i in range(data['N'])]
y = pulp.LpVariable('y', lowBound=0, upBound=data['MaxOvertimeAssembly'], cat='Integer')

# Objective function
total_material_cost = pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N']))
discount_condition = total_material_cost > data['DiscountThreshold']
material_discount = data['MaterialDiscount'] / 100

# Calculate delta
delta = pulp.LpVariable("delta", lowBound=0, upBound=material_discount, cat='Continuous')
problem += delta == material_discount * discount_condition

total_profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) \
               - pulp.lpSum(data['MaterialCost'][i] * x[i] * (1 - delta) for i in range(data['N'])) \
               - data['OvertimeAssemblyCost'] * y

problem += total_profit

# Constraints
problem += pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) <= data['MaxAssembly'] + y
problem += pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting']

# Solve
problem.solve()

# Print the objective value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
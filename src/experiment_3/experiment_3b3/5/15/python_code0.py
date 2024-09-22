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

# Model initialization
problem = pulp.LpProblem("Company_Production", pulp.LpMaximize)

# Variables
x = [pulp.LpVariable(f'x{i}', lowBound=0, cat='Integer') for i in range(data['N'])]
o = pulp.LpVariable('o', lowBound=0, cat='Continuous')
m = pulp.LpVariable('m', lowBound=0, cat='Continuous')

# Objective Function
material_cost_x = [data['MaterialCost'][i] * x[i] for i in range(data['N'])]
total_material_cost = pulp.lpSum(material_cost_x)
discount = pulp.LpVariable('Discount', lowBound=0, cat='Continuous')

profit_without_discount = pulp.lpSum([data['Price'][i] * x[i] for i in range(data['N'])]) - total_material_cost + discount - data['OvertimeAssemblyCost'] * o
problem += profit_without_discount

# Constraints
problem += pulp.lpSum([data['AssemblyHour'][i] * x[i] for i in range(data['N'])]) + o <= data['MaxAssembly'] + data['MaxOvertimeAssembly']
problem += pulp.lpSum([data['TestingHour'][i] * x[i] for i in range(data['N'])]) <= data['MaxTesting']
problem += m == total_material_cost

# Discount condition
problem += discount <= (data['MaterialDiscount'] / 100) * total_material_cost
problem += discount <= (total_material_cost - data['DiscountThreshold']) * (total_material_cost >= data['DiscountThreshold'])

# Solve the problem
problem.solve()

# Output
units_produced = [pulp.value(x[i]) for i in range(data['N'])]
daily_profit = pulp.value(problem.objective)
overtime_assembly = pulp.value(o)
material_bought = pulp.value(m)

print(f'Units Produced: {units_produced}')
print(f'Overtime Assembly: {overtime_assembly}')
print(f'Material Bought: {material_bought}')
print(f'Daily Profit (Objective Value): <OBJ>{daily_profit}</OBJ>')
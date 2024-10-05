import pulp

# Input data
data = {
    'N': 2, 
    'assemblyHour': [0.25, 0.3333], 
    'testingHour': [0.125, 0.3333], 
    'materialCost': [1.2, 0.9], 
    'maxAssembly': 10, 
    'maxTesting': 70, 
    'price': [9, 8], 
    'maxOvertimeAssembly': 50, 
    'overtimeAssemblyCost': 5, 
    'materialDiscount': 10, 
    'discountThreshold': 300
}

# Problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
unitsProduced = [pulp.LpVariable(f'x{i}', lowBound=0, cat='Integer') for i in range(data['N'])]
overtimeAssembly = pulp.LpVariable('overtimeAssembly', lowBound=0, upBound=data['maxOvertimeAssembly'], cat='Continuous')

# Objective function
total_revenue = pulp.lpSum([data['price'][i] * unitsProduced[i] for i in range(data['N'])])
total_material_cost = pulp.lpSum([data['materialCost'][i] * unitsProduced[i] for i in range(data['N'])])

# Calculate total material cost with discount consideration
material_cost = total_material_cost
discount_condition = material_cost >= data['discountThreshold']
discounted_material_cost = material_cost * (1 - data['materialDiscount'] / 100)

# Total cost calculation
total_cost = total_material_cost - pulp.LpAffineExpression([(-discounted_material_cost, discount_condition)])

total_overtime_cost = overtimeAssembly * data['overtimeAssemblyCost']
profit = total_revenue - total_cost - total_overtime_cost

problem += profit

# Constraints
problem += pulp.lpSum([data['assemblyHour'][i] * unitsProduced[i] for i in range(data['N'])]) + overtimeAssembly <= data['maxAssembly']
problem += pulp.lpSum([data['testingHour'][i] * unitsProduced[i] for i in range(data['N'])]) <= data['maxTesting']

# Solve the problem
problem.solve()

# Extract results
results = {
    "dailyProfit": pulp.value(problem.objective),
    "unitsProduced": [unitsProduced[i].varValue for i in range(data['N'])],
    "overtimeAssembly": overtimeAssembly.varValue,
    "materialBought": pulp.value(total_material_cost)
}

print(results)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
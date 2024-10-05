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

# Apply discount if material cost is above the discountThreshold
discounted_material_cost = pulp.lpSum(total_material_cost * (1 - data['materialDiscount'] / 100))
material_cost = pulp.lpSum([pulp.lpSum([data['materialCost'][i] * unitsProduced[i]]) for i in range(data['N'])])
material_cost = pulp.lpSum([discounted_material_cost if material_cost > data['discountThreshold'] else material_cost])

total_assembly_hours = pulp.lpSum([data['assemblyHour'][i] * unitsProduced[i] for i in range(data['N'])]) + overtimeAssembly
total_testing_hours = pulp.lpSum([data['testingHour'][i] * unitsProduced[i] for i in range(data['N'])])
total_overtime_cost = overtimeAssembly * data['overtimeAssemblyCost']

problem += total_revenue - material_cost - total_overtime_cost

# Constraints
problem += total_assembly_hours <= data['maxAssembly'] + overtimeAssembly
problem += total_testing_hours <= data['maxTesting']

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
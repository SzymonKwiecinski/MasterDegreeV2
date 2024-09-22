import pulp

# Define the data
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

# Define variables
unitsProduced = [pulp.LpVariable(f'unitsProduced_{i}', lowBound=0, cat='Integer') for i in range(data['N'])]
overtimeAssembly = pulp.LpVariable('overtimeAssembly', lowBound=0, cat='Integer')
discountApplied = pulp.LpVariable('discountApplied', cat='Binary')

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Total Material Cost
totalMaterialCost = pulp.lpSum(data['MaterialCost'][i] * unitsProduced[i] for i in range(data['N']))

# Material Cost with Discount
materialCost = totalMaterialCost * (1 - discountApplied * data['MaterialDiscount'] / 100.0)

# Overtime Cost
overtimeCost = overtimeAssembly * data['OvertimeAssemblyCost']

# Total Cost
totalCost = materialCost + overtimeCost

# Revenue
revenue = pulp.lpSum(data['Price'][i] * unitsProduced[i] for i in range(data['N']))

# Objective function
profit = revenue - totalCost
problem += profit

# Constraints
# Assembly hours constraint
problem += pulp.lpSum(data['AssemblyHour'][i] * unitsProduced[i] for i in range(data['N'])) <= data['MaxAssembly'] + overtimeAssembly

# Testing hours constraint
problem += pulp.lpSum(data['TestingHour'][i] * unitsProduced[i] for i in range(data['N'])) <= data['MaxTesting']

# Overtime assembly constraint
problem += overtimeAssembly <= data['MaxOvertimeAssembly']

# Material discount constraints
problem += (totalMaterialCost > data['DiscountThreshold'] - 1e-5) <= discountApplied
problem += (totalMaterialCost <= data['DiscountThreshold'] + 1e-5) >= (1 - discountApplied)

# Solve the problem
problem.solve(pulp.PULP_CBC_CMD(msg=0))

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
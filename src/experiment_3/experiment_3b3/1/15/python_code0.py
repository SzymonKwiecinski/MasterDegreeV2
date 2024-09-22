import pulp

# Extracting data
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

# Defining the problem
problem = pulp.LpProblem("ProductionOptimization", pulp.LpMaximize)

# Decision Variables
unitsProduced = [pulp.LpVariable(f'unitsProduced_{i}', lowBound=0, cat='Integer') for i in range(data['N'])]
overtimeAssembly = pulp.LpVariable('overtimeAssembly', lowBound=0, upBound=data['MaxOvertimeAssembly'], cat='Continuous')
materialBought = pulp.LpVariable('materialBought', lowBound=0, cat='Continuous')

# Objective Function
profit = pulp.lpSum(data['Price'][i] * unitsProduced[i] for i in range(data['N'])) - materialBought - (overtimeAssembly * data['OvertimeAssemblyCost'])
problem += profit

# Constraints

# Assembly hours constraint including overtime
problem += (pulp.lpSum(data['AssemblyHour'][i] * unitsProduced[i] for i in range(data['N'])) + overtimeAssembly 
            <= data['MaxAssembly'] + data['MaxOvertimeAssembly'])

# Testing hours constraint
problem += (pulp.lpSum(data['TestingHour'][i] * unitsProduced[i] for i in range(data['N'])) <= data['MaxTesting'])

# Material cost with discount application
material_cost_no_discount = pulp.lpSum(data['MaterialCost'][i] * unitsProduced[i] for i in range(data['N']))
discounted_material_cost = material_cost_no_discount * (1 - data['MaterialDiscount'] / 100)

# Conditional constraint for material bought
problem += (materialBought >= discounted_material_cost, "MaterialDiscountConditional") 
problem += (materialBought >= material_cost_no_discount, "MaterialCostNoDiscount")

# Solve the problem
problem.solve()

# Output Results
print(f'unitsProduced: {[pulp.value(unitsProduced[i]) for i in range(data["N"])]}')
print(f'overtimeAssembly: {pulp.value(overtimeAssembly)}')
print(f'materialBought: {pulp.value(materialBought)}')
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
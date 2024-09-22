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

# Create the LP problem
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

# Decision Variables
unitsProduced = [pulp.LpVariable(f'unitsProduced_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]
overtimeAssembly = pulp.LpVariable('overtimeAssembly', lowBound=0, cat='Continuous')
materialBought = pulp.LpVariable('materialBought', cat='Continuous')

# Objective Function
profit_terms = [data['Price'][i] * unitsProduced[i] for i in range(data['N'])]
cost_terms = [data['MaterialCost'][i] * unitsProduced[i] * (1 - data['MaterialDiscount'] / 100) for i in range(data['N'])]
objective = pulp.lpSum(profit_terms) - (pulp.lpSum(cost_terms) + overtimeAssembly * data['OvertimeAssemblyCost'])
problem += objective

# Constraints
problem += (pulp.lpSum(data['AssemblyHour'][i] * unitsProduced[i] for i in range(data['N'])) + overtimeAssembly 
            <= data['MaxAssembly'] + data['MaxOvertimeAssembly'], "Assembly_Labor_Constraint")

problem += (pulp.lpSum(data['TestingHour'][i] * unitsProduced[i] for i in range(data['N'])) 
            <= data['MaxTesting'], "Testing_Labor_Constraint")

problem += (materialBought == pulp.lpSum(data['MaterialCost'][i] * unitsProduced[i] for i in range(data['N'])), 
            "Material_Bought_Constraint")

# Solve the problem
problem.solve()

# Output results
unitsProduced_result = [unitsProduced[i].varValue for i in range(data['N'])]
overtimeAssembly_result = overtimeAssembly.varValue
materialBought_result = materialBought.varValue

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Units Produced: {unitsProduced_result}')
print(f'Overtime Assembly Hours: {overtimeAssembly_result}')
print(f'Material Bought: {materialBought_result}')
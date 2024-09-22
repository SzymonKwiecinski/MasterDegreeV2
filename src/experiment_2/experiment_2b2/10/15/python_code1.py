import pulp

# Extract data
data = {'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}

N = data['N']
assemblyHour = data['AssemblyHour']
testingHour = data['TestingHour']
materialCost = data['MaterialCost']
maxAssembly = data['MaxAssembly']
maxTesting = data['MaxTesting']
price = data['Price']
maxOvertimeAssembly = data['MaxOvertimeAssembly']
overtimeAssemblyCost = data['OvertimeAssemblyCost']
materialDiscount = data['MaterialDiscount']
discountThreshold = data['DiscountThreshold']

# Define problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
unitsProduced = [pulp.LpVariable(f"unitsProduced_{i}", lowBound=0, cat='Continuous') for i in range(N)]
overtimeAssembly = pulp.LpVariable("overtimeAssembly", lowBound=0, upBound=maxOvertimeAssembly, cat='Continuous')
materialBought = pulp.LpVariable("materialBought", lowBound=0, cat='Continuous')

# Objective function
revenue = pulp.lpSum([price[i] * unitsProduced[i] for i in range(N)])
totalMaterialCost = pulp.lpSum([materialCost[i] * unitsProduced[i] for i in range(N)])

# Apply discount only if totalMaterialCost exceeds the discount threshold
discountedMaterialCost = totalMaterialCost - materialBought
problem += materialBought >= totalMaterialCost - (materialDiscount / 100) * totalMaterialCost
problem += materialBought >= totalMaterialCost - (materialDiscount / 100) * discountThreshold

overtimeCost = overtimeAssembly * overtimeAssemblyCost

profit = revenue - discountedMaterialCost - overtimeCost

problem += profit

# Constraints
problem += pulp.lpSum([assemblyHour[i] * unitsProduced[i] for i in range(N)]) <= maxAssembly + overtimeAssembly
problem += pulp.lpSum([testingHour[i] * unitsProduced[i] for i in range(N)]) <= maxTesting

# Solve problem
problem.solve()

# Output results
dailyProfit = pulp.value(problem.objective)
unitsProduced_values = [pulp.value(unitsProduced[i]) for i in range(N)]
overtimeAssembly_value = pulp.value(overtimeAssembly)
materialBought_value = pulp.value(materialBought)

output = {
    "dailyProfit": dailyProfit,
    "unitsProduced": unitsProduced_values,
    "overtimeAssembly": overtimeAssembly_value,
    "materialBought": materialBought_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
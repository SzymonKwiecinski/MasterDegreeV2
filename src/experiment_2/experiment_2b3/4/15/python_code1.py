import pulp

# Data
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

# Problem
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

# Variables
unitsProduced = [pulp.LpVariable(f'UnitsProduced_{i}', lowBound=0, cat='Integer') for i in range(N)]
overtimeAssembly = pulp.LpVariable('OvertimeAssembly', lowBound=0, cat='Continuous')

# Constraints
problem += pulp.lpSum(assemblyHour[i] * unitsProduced[i] for i in range(N)) <= maxAssembly + overtimeAssembly
problem += pulp.lpSum(testingHour[i] * unitsProduced[i] for i in range(N)) <= maxTesting
problem += overtimeAssembly <= maxOvertimeAssembly

# Objective function
materialBought = pulp.lpSum(materialCost[i] * unitsProduced[i] for i in range(N))
totalRevenue = pulp.lpSum(price[i] * unitsProduced[i] for i in range(N))
totalCost = materialBought + overtimeAssembly * overtimeAssemblyCost

# Apply discount if applicable
discount = pulp.LpVariable('Discount', lowBound=0)
problem += discount == (materialBought * materialDiscount / 100) * (materialBought > discountThreshold)

dailyProfit = totalRevenue - (totalCost - discount)

problem += dailyProfit

# Solve the problem
problem.solve()

# Output
dailyProfit_value = pulp.value(dailyProfit)
unitsProduced_values = [pulp.value(unitsProduced[i]) for i in range(N)]
overtimeAssembly_value = pulp.value(overtimeAssembly)
materialBought_value = pulp.value(materialBought)

output = {
    "dailyProfit": dailyProfit_value,
    "unitsProduced": unitsProduced_values,
    "overtimeAssembly": overtimeAssembly_value,
    "materialBought": materialBought_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
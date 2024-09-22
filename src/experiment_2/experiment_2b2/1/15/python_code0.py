import pulp

# Problem Data
data = {'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}

# Unpack the data
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

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
unitsProduced = [pulp.LpVariable(f'Units_Produced_{i}', lowBound=0, cat='Integer') for i in range(N)]
overtimeAssembly = pulp.LpVariable('Overtime_Assembly', lowBound=0, upBound=maxOvertimeAssembly, cat='Continuous')

# Revenue
revenue = pulp.lpSum([price[i] * unitsProduced[i] for i in range(N)])

# Total Material Cost
materialCostTotal = pulp.lpSum([materialCost[i] * unitsProduced[i] for i in range(N)])
discountedMaterialCostTotal = pulp.LpAffineExpression(materialCostTotal)
# Apply the discount if total material cost is above the threshold
if materialCostTotal >= discountThreshold:
    discountedMaterialCostTotal *= (1 - materialDiscount / 100.0)

# Total Overtime Cost
overtimeCost = overtimeAssembly * overtimeAssemblyCost

# Objective Function: Maximize Profit
problem += revenue - (discountedMaterialCostTotal + overtimeCost), 'Profit'

# Constraints
# Max Assembly Hours (including overtime)
problem += pulp.lpSum([assemblyHour[i] * unitsProduced[i] for i in range(N)]) <= maxAssembly + overtimeAssembly, 'Max_Assembly_Hours'
# Max Testing Hours
problem += pulp.lpSum([testingHour[i] * unitsProduced[i] for i in range(N)]) <= maxTesting, 'Max_Testing_Hours'

# Solve the problem
problem.solve()

# Output results
dailyProfit = pulp.value(problem.objective)
unitsProduced_values = [pulp.value(unitsProduced[i]) for i in range(N)]
overtimeAssembly_value = pulp.value(overtimeAssembly)
materialBought_value = pulp.value(pulp.lpSum([materialCost[i] * unitsProduced[i] for i in range(N)]))

result = {
    "dailyProfit": dailyProfit,
    "unitsProduced": unitsProduced_values,
    "overtimeAssembly": overtimeAssembly_value,
    "materialBought": materialBought_value
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
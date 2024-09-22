import json
import pulp

# Input data
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

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
unitsProduced = [pulp.LpVariable(f'unitsProduced_{i}', lowBound=0, cat='Integer') for i in range(data['N'])]
overtimeAssembly = pulp.LpVariable('overtimeAssembly', lowBound=0, upBound=data['MaxOvertimeAssembly'], cat='Continuous')

# Total costs and revenues
totalRevenue = pulp.lpSum(unitsProduced[i] * data['Price'][i] for i in range(data['N']))
totalMaterialCost = pulp.lpSum(unitsProduced[i] * data['MaterialCost'][i] for i in range(data['N']))

# Applying material discount
totalMaterialCostDiscounted = totalMaterialCost * (1 - data['MaterialDiscount'] / 100) if totalMaterialCost > data['DiscountThreshold'] else totalMaterialCost

totalAssemblyCost = pulp.lpSum(unitsProduced[i] * data['AssemblyHour'][i] for i in range(data['N'])) + overtimeAssembly * data['OvertimeAssemblyCost']

# Objective function
problem += totalRevenue - (totalMaterialCostDiscounted + totalAssemblyCost), "Total_Profit"

# Constraints
problem += pulp.lpSum(unitsProduced[i] * data['AssemblyHour'][i] for i in range(data['N'])) + overtimeAssembly <= data['MaxAssembly'], "MaxAssemblyConstraint"
problem += pulp.lpSum(unitsProduced[i] * data['TestingHour'][i] for i in range(data['N'])) <= data['MaxTesting'], "MaxTestingConstraint"

# Solve the problem
problem.solve()

# Output results
dailyProfit = pulp.value(problem.objective)
unitsProducedResult = [pulp.value(unitsProduced[i]) for i in range(data['N'])]
overtimeAssemblyResult = pulp.value(overtimeAssembly)
materialBought = pulp.value(totalMaterialCostDiscounted)

print(f' (Objective Value): <OBJ>{dailyProfit}</OBJ>')
output = {
    "dailyProfit": dailyProfit,
    "unitsProduced": unitsProducedResult,
    "overtimeAssembly": overtimeAssemblyResult,
    "materialBought": materialBought
}
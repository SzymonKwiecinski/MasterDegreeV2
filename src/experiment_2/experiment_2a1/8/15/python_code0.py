import pulp
import json

# Input data in JSON format
data = {'N': 2, 
        'AssemblyHour': [0.25, 0.3333], 
        'TestingHour': [0.125, 0.3333], 
        'MaterialCost': [1.2, 0.9], 
        'MaxAssembly': 10, 
        'MaxTesting': 70, 
        'Price': [9, 8], 
        'MaxOvertimeAssembly': 50, 
        'OvertimeAssemblyCost': 5, 
        'MaterialDiscount': 10, 
        'DiscountThreshold': 300}

# Initialize the problem
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

# Variables
N = data['N']
unitsProduced = [pulp.LpVariable(f'unitsProduced_{i}', lowBound=0, cat='Integer') for i in range(N)]
overtimeAssembly = pulp.LpVariable('overtimeAssembly', lowBound=0, upBound=data['MaxOvertimeAssembly'], cat='Continuous')

# Costs and revenues
materialCost = data['MaterialCost']
price = data['Price']
assemblyHour = data['AssemblyHour']
testingHour = data['TestingHour']

# Constraints
problem += pulp.lpSum([assemblyHour[i] * unitsProduced[i] for i in range(N)]) + overtimeAssembly <= data['MaxAssembly'], "MaxAssemblyConstraint"
problem += pulp.lpSum([testingHour[i] * unitsProduced[i] for i in range(N)]) <= data['MaxTesting'], "MaxTestingConstraint"

# Objective Function
totalRevenue = pulp.lpSum([price[i] * unitsProduced[i] for i in range(N)])
totalMaterialCost = pulp.lpSum([materialCost[i] * unitsProduced[i] for i in range(N)])
totalCost = totalMaterialCost + overtimeAssembly * data['OvertimeAssemblyCost']

# Calculate discount if applicable
totalCostWithDiscount = totalCost
if totalMaterialCost > data['DiscountThreshold']:
    totalCostWithDiscount *= (1 - (data['MaterialDiscount'] / 100))

# Profit function
dailyProfit = totalRevenue - totalCostWithDiscount
problem += dailyProfit, "Objective"

# Solve the problem
problem.solve()

# Output results
unitsProduced_solution = [pulp.value(unitsProduced[i]) for i in range(N)]
overtimeAssembly_solution = pulp.value(overtimeAssembly)
materialBought = sum(pulp.value(unitsProduced[i]) * materialCost[i] for i in range(N))

# Print the results
print(json.dumps({
    "dailyProfit": pulp.value(problem.objective),
    "unitsProduced": unitsProduced_solution,
    "overtimeAssembly": overtimeAssembly_solution,
    "materialBought": materialBought
}))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
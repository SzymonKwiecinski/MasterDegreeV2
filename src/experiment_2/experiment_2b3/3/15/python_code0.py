import pulp

# Parse the input data
data = {'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 
        'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 
        'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 
        'MaterialDiscount': 10, 'DiscountThreshold': 300}

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

# Decision variables
unitsProduced = [pulp.LpVariable(f'UnitsProduced_{i}', lowBound=0, cat='Continuous') for i in range(N)]
overtimeAssembly = pulp.LpVariable('OvertimeAssembly', lowBound=0, upBound=maxOvertimeAssembly, cat='Continuous')

# Constraints
# Assembly constraint
problem += pulp.lpSum([assemblyHour[i] * unitsProduced[i] for i in range(N)]) <= maxAssembly + overtimeAssembly
# Testing constraint
problem += pulp.lpSum([testingHour[i] * unitsProduced[i] for i in range(N)]) <= maxTesting

# Objective function - revenue minus costs
revenue = pulp.lpSum([price[i] * unitsProduced[i] for i in range(N)])
materialBought = pulp.lpSum([materialCost[i] * unitsProduced[i] for i in range(N)])
if materialBought > discountThreshold:
    materialBought *= (1 - materialDiscount / 100)
overtimeCost = overtimeAssembly * overtimeAssemblyCost

problem += revenue - (materialBought + overtimeCost)

# Solve the problem
problem.solve()

# Results
dailyProfit = pulp.value(problem.objective)
unitsProduced_values = [pulp.value(unitsProduced[i]) for i in range(N)]
overtimeAssembly_value = pulp.value(overtimeAssembly)
materialBought_value = materialBought

output = {
    "dailyProfit": dailyProfit,
    "unitsProduced": unitsProduced_values,
    "overtimeAssembly": overtimeAssembly_value,
    "materialBought": materialBought_value
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
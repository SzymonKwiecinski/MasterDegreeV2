import pulp

# Define the problem
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

# Data input
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

# Decision variables
unitsProduced = [pulp.LpVariable(f'UnitsProduced_{i}', lowBound=0, cat='Integer') for i in range(N)]
overtimeAssembly = pulp.LpVariable('OvertimeAssembly', lowBound=0, upBound=maxOvertimeAssembly, cat='Integer')
materialBought = pulp.lpSum([materialCost[i] * unitsProduced[i] for i in range(N)])

# Objective function
revenue = pulp.lpSum([price[i] * unitsProduced[i] for i in range(N)])
total_cost = materialBought + overtimeAssembly * overtimeAssemblyCost
if materialBought > discountThreshold:
    total_cost *= (1 - materialDiscount / 100)

profit = revenue - total_cost
problem += profit

# Constraints
problem += pulp.lpSum([assemblyHour[i] * unitsProduced[i] for i in range(N)]) <= maxAssembly + overtimeAssembly
problem += pulp.lpSum([testingHour[i] * unitsProduced[i] for i in range(N)]) <= maxTesting

# Solve the problem
problem.solve()

# Output results
result = {
    "dailyProfit": pulp.value(problem.objective),
    "unitsProduced": [pulp.value(unitsProduced[i]) for i in range(N)],
    "overtimeAssembly": pulp.value(overtimeAssembly),
    "materialBought": pulp.value(materialBought)
}

print(result)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
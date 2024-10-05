import pulp

# Data input from JSON
data = {'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}

# Extract values from data
N = data["N"]
assemblyHour = data["AssemblyHour"]
testingHour = data["TestingHour"]
materialCost = data["MaterialCost"]
maxAssembly = data["MaxAssembly"]
maxTesting = data["MaxTesting"]
price = data["Price"]
maxOvertimeAssembly = data["MaxOvertimeAssembly"]
overtimeAssemblyCost = data["OvertimeAssemblyCost"]
materialDiscount = data["MaterialDiscount"]
discountThreshold = data["DiscountThreshold"]

# Create the optimization problem
problem = pulp.LpProblem("Daily_Profit_Maximization", pulp.LpMaximize)

# Variables
unitsProduced = [pulp.LpVariable(f'UnitsProduced_{i}', lowBound=0, cat='Integer') for i in range(N)]
overtimeAssembly = pulp.LpVariable('OvertimeAssembly', lowBound=0, upBound=maxOvertimeAssembly, cat='Continuous')
materialBought = pulp.LpVariable('MaterialBought', lowBound=0, cat='Continuous')

# Objective Function: Maximize profit
material_cost = pulp.lpSum([materialCost[i] * unitsProduced[i] for i in range(N)])
discount = pulp.lpSum([materialCost[i] * unitsProduced[i] for i in range(N)]) > discountThreshold
revenue = pulp.lpSum([price[i] * unitsProduced[i] for i in range(N)])
overtimeCost = overtimeAssemblyCost * overtimeAssembly

problem += revenue - material_cost * (1 - materialDiscount / 100) * discount - material_cost * (1 - discount) - overtimeCost, "DailyProfit"

# Constraints
problem += pulp.lpSum([assemblyHour[i] * unitsProduced[i] for i in range(N)]) <= maxAssembly + overtimeAssembly, "AssemblyTimeConstraint"
problem += pulp.lpSum([testingHour[i] * unitsProduced[i] for i in range(N)]) <= maxTesting, "TestingTimeConstraint"
problem += materialBought == pulp.lpSum([materialCost[i] * unitsProduced[i] for i in range(N)]), "MaterialBoughtConstraint"

# Solve the problem
problem.solve()

# Results
result = {
    "dailyProfit": pulp.value(problem.objective),
    "unitsProduced": [pulp.value(unitsProduced[i]) for i in range(N)],
    "overtimeAssembly": pulp.value(overtimeAssembly),
    "materialBought": pulp.value(materialBought)
}

print(result)
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
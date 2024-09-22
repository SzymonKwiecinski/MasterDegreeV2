import pulp

# Define the data
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

# Create the problem variable to contain the optimization problem data
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Decision variables for amount of product i
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Integer') for i in range(data['N'])]

# Overtime assembly hours used
overtimeAssembly = pulp.LpVariable("overtimeAssembly", lowBound=0, cat='Continuous')

# Calculate total material cost
totalMaterialCost = pulp.lpSum([data['MaterialCost'][i] * x[i] for i in range(data['N'])])

# Apply material discount
discountedMaterialCost = totalMaterialCost
if pulp.value(totalMaterialCost) > data['DiscountThreshold']:
    discountedMaterialCost *= (1 - data['MaterialDiscount'] / 100)

# Objective function
totalRevenue = pulp.lpSum([data['Price'][i] * x[i] for i in range(data['N'])])
totalCost = discountedMaterialCost + overtimeAssembly * data['OvertimeAssemblyCost']
dailyProfit = totalRevenue - totalCost
problem += dailyProfit, "Objective: Maximize Daily Profit"

# Constraints
problem += pulp.lpSum([data['AssemblyHour'][i] * x[i] for i in range(data['N'])]) + overtimeAssembly <= data['MaxAssembly'] + data['MaxOvertimeAssembly'], "Assembly Hours Constraint"
problem += pulp.lpSum([data['TestingHour'][i] * x[i] for i in range(data['N'])]) <= data['MaxTesting'], "Testing Hours Constraint"

# Solve the problem
problem.solve()

# Print results
print(f"Units Produced: {[pulp.value(x[i]) for i in range(data['N'])]}")
print(f"Overtime Assembly Used: {pulp.value(overtimeAssembly)}")
print(f"Material Bought: {pulp.value(totalMaterialCost)}")
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
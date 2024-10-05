import pulp

# Read data from JSON format
data = {'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}

# Problem definition
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

# Decision variables
units = [pulp.LpVariable(f"unitsProduced_{i}", lowBound=0, cat='Integer') for i in range(data['N'])]
overtimeAssembly = pulp.LpVariable("overtimeAssembly", lowBound=0, upBound=data['MaxOvertimeAssembly'], cat='Continuous')

# Objective function
total_revenue = pulp.lpSum([units[i] * data['Price'][i] for i in range(data['N'])])
total_material_cost = pulp.lpSum([units[i] * data['MaterialCost'][i] for i in range(data['N'])])

if total_material_cost > data['DiscountThreshold']:
    total_material_cost *= (1 - data['MaterialDiscount'] / 100)

total_cost = total_material_cost + overtimeAssembly * data['OvertimeAssemblyCost']
profit = total_revenue - total_cost

problem += profit

# Constraints
problem += pulp.lpSum([units[i] * data['AssemblyHour'][i] for i in range(data['N'])]) <= data['MaxAssembly'] + overtimeAssembly
problem += pulp.lpSum([units[i] * data['TestingHour'][i] for i in range(data['N'])]) <= data['MaxTesting']

# Solve the problem
problem.solve()

# Prepare the output
solution = {
    "dailyProfit": pulp.value(profit),
    "unitsProduced": [pulp.value(units[i]) for i in range(data['N'])],
    "overtimeAssembly": pulp.value(overtimeAssembly),
    "materialBought": sum([pulp.value(units[i]) * data['MaterialCost'][i] for i in range(data['N'])])
}

print(solution)
# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
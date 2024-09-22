import pulp

# Data from the provided JSON
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

# Problem definition
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

# Decision variables
unitsProduced = pulp.LpVariable.dicts("unitsProduced", range(1, data['N'] + 1), lowBound=0, cat='Integer')
overtimeAssembly = pulp.LpVariable("overtimeAssembly", lowBound=0, upBound=data['MaxOvertimeAssembly'], cat='Continuous')

# Objective function
materialBought = pulp.lpSum(data['MaterialCost'][i-1] * unitsProduced[i] for i in range(1, data['N'] + 1))
profit = pulp.lpSum(data['Price'][i-1] * unitsProduced[i] for i in range(1, data['N'] + 1)) - materialBought - (data['OvertimeAssemblyCost'] * overtimeAssembly)

# Apply discount if conditions are met
if materialBought > data['DiscountThreshold']:
    materialBought = materialBought * (1 - data['MaterialDiscount'] / 100)

problem += profit, "Total Profit"

# Constraints
problem += pulp.lpSum(data['AssemblyHour'][i-1] * unitsProduced[i] for i in range(1, data['N'] + 1)) <= data['MaxAssembly'] + overtimeAssembly, "Assembly_Hours_Constraint"
problem += pulp.lpSum(data['TestingHour'][i-1] * unitsProduced[i] for i in range(1, data['N'] + 1)) <= data['MaxTesting'], "Testing_Hours_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
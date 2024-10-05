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

# Create the LP problem
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

# Decision Variables
unitsProduced = pulp.LpVariable.dicts("unitsProduced", range(data['N']), lowBound=0, cat='Integer')
overtimeAssembly = pulp.LpVariable("overtimeAssembly", lowBound=0)
materialBought = pulp.LpVariable("materialBought", lowBound=0)

# Objective Function
profit = pulp.lpSum(data['Price'][i] * unitsProduced[i] for i in range(data['N'])) \
         - (1 - data['MaterialDiscount'] / 100) * materialBought \
         - data['OvertimeAssemblyCost'] * overtimeAssembly

problem += profit

# Constraints
problem += (pulp.lpSum(data['AssemblyHour'][i] * unitsProduced[i] for i in range(data['N'])) 
             <= data['MaxAssembly'] + overtimeAssembly)

problem += (pulp.lpSum(data['TestingHour'][i] * unitsProduced[i] for i in range(data['N'])) 
             <= data['MaxTesting'])

problem += overtimeAssembly <= data['MaxOvertimeAssembly']

problem += materialBought == pulp.lpSum(data['MaterialCost'][i] * unitsProduced[i] for i in range(data['N']))

# Apply discount condition
discount_condition = (materialBought > data['DiscountThreshold'])
problem += materialBought == pulp.lpSum(data['MaterialCost'][i] * unitsProduced[i] for i in range(data['N'])) * pulp.lpSum([1 - data['MaterialDiscount'] / 100 if discount_condition else 1 for i in range(data['N'])])

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
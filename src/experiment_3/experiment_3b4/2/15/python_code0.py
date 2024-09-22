import pulp

# Data
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
    'MaterialDiscount': 0.10,
    'DiscountThreshold': 300
}

# Indices and sets
N = range(data['N'])

# Problem
problem = pulp.LpProblem("Profit_Maximization", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat=pulp.LpContinuous) for i in N]
overtime_assembly = pulp.LpVariable('overtimeAssembly', lowBound=0, upBound=data['MaxOvertimeAssembly'], cat=pulp.LpContinuous)
y = pulp.LpVariable('y', cat=pulp.LpBinary)

# Objective Function
profit = pulp.lpSum([data['Price'][i] * x[i] for i in N]) - \
         (1 - data['MaterialDiscount'] * y) * pulp.lpSum([data['MaterialCost'][i] * x[i] for i in N]) - \
         data['OvertimeAssemblyCost'] * overtime_assembly
problem += profit

# Constraints
# Assembly hours
problem += (pulp.lpSum([data['AssemblyHour'][i] * x[i] for i in N]) <= data['MaxAssembly'] + overtime_assembly)

# Testing hours
problem += (pulp.lpSum([data['TestingHour'][i] * x[i] for i in N]) <= data['MaxTesting'])

# Big-M constraint for material discount
M = sum(data['MaterialCost']) * 1000  # A sufficiently large constant
problem += (data['MaterialDiscount'] * (pulp.lpSum([data['MaterialCost'][i] * x[i] for i in N]) - data['DiscountThreshold']) <= M * y)

# Discount threshold constraint
problem += (pulp.lpSum([data['MaterialCost'][i] * x[i] for i in N]) >= data['DiscountThreshold'] * y)

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
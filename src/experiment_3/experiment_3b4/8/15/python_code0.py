import pulp

# Data from JSON
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

# Number of product types
N = data['N']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i+1}', lowBound=0, cat='Integer') for i in range(N)]
z = pulp.LpVariable('z', lowBound=0, cat='Integer')

# Objective function
material_cost = pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(N))
profit = pulp.lpSum((data['Price'][i] - data['MaterialCost'][i]) * x[i] for i in range(N)) - data['OvertimeAssemblyCost'] * z
problem += profit

# Constraints

# Assembly Labor Constraint
problem += pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(N)) <= data['MaxAssembly'] + z

# Overtime constraint
problem += z <= data['MaxOvertimeAssembly']

# Testing Constraint
problem += pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(N)) <= data['MaxTesting']

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
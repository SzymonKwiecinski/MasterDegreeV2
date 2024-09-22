import pulp

# Data from JSON
data = {'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 
        'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 
        'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 
        'MaterialDiscount': 10, 'DiscountThreshold': 300}

# Initialize the problem
problem = pulp.LpProblem("Profit_Maximization", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]
y = pulp.LpVariable("y", lowBound=0, cat='Continuous')

# Objective Function
material_cost_total = pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N']))
discount = pulp.lpSum((data['MaterialDiscount'] / 100) * material_cost_total) if material_cost_total > data['DiscountThreshold'] else 0
Z = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) - (material_cost_total - discount + y * data['OvertimeAssemblyCost'])
problem += Z

# Constraints
assembly_constraint = pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + y <= data['MaxAssembly'] + data['MaxOvertimeAssembly']
problem += assembly_constraint

testing_constraint = pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting']
problem += testing_constraint

# Solve the problem
problem.solve()

# Print objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp

# Data from JSON format
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

# Create a problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Integer') for i in range(data['N'])]
y = pulp.LpVariable('y', lowBound=0, upBound=data['MaxOvertimeAssembly'], cat='Integer')

# Objective Function
# Calculate total material cost with condition for discount
material_cost_expr = pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N']))
total_material_cost = pulp.lpSum((1 - data['MaterialDiscount'] / 100) * material_cost_expr) \
                       if pulp.value(material_cost_expr) > data['DiscountThreshold'] else material_cost_expr

profit_expr = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) - total_material_cost - (data['OvertimeAssemblyCost'] * y)

problem += profit_expr

# Constraints
# Assembly labor time constraint
problem += pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) <= data['MaxAssembly'] + y, "Assembly_Time_Constraint"

# Testing labor time constraint
problem += pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting'], "Testing_Time_Constraint"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
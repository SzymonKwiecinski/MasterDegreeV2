import pulp

# Data extracted from JSON format
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

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0)  # Units produced of each product
O = pulp.LpVariable("O", lowBound=0)  # Overtime hours

# Objective function
material_cost = pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N']))
total_revenue = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))

# Discount application
discount = pulp.if_then(material_cost <= data['DiscountThreshold'], 0)
discount += pulp.if_then(material_cost > data['DiscountThreshold'], (data['MaterialDiscount'] / 100.0) * material_cost)

# Objective function formulation
profit = total_revenue - (material_cost - discount) - (data['OvertimeAssemblyCost'] * O)
problem += profit, "Profit"

# Constraints
# Assembly labor constraint
problem += (pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + O <= data['MaxAssembly'] + data['MaxOvertimeAssembly']), "Assembly_Labor"

# Testing labor constraint
problem += (pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting']), "Testing_Labor"

# Solve the problem
problem.solve()

# Print results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
units_produced = [pulp.value(x[i]) for i in range(data['N'])]
overtime_hours = pulp.value(O)
material_bought = pulp.value(material_cost)

print(f"Units Produced: {units_produced}")
print(f"Overtime Hours: {overtime_hours}")
print(f"Material Bought: {material_bought}")
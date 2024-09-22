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
    'MaterialDiscount': 10,
    'DiscountThreshold': 300
}

# Problem definition
problem = pulp.LpProblem("Production_Problem", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0, cat='Continuous')
overtimeAssembly = pulp.LpVariable("overtimeAssembly", lowBound=0, cat='Continuous')

# Objective Function
material_cost_total = pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N']))
total_price = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))

# Discount calculation
discount = pulp.lpSum([data['MaterialDiscount'] / 100 * material_cost_total if material_cost_total > data['DiscountThreshold'] else 0])

# Profit function
profit = total_price - (material_cost_total - discount) - (data['OvertimeAssemblyCost'] * overtimeAssembly)
problem += profit, "Total_Profit"

# Constraints
problem += (pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + overtimeAssembly <= data['MaxAssembly'] + data['MaxOvertimeAssembly']), "Assembly_Hours_Constraint"
problem += (pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting']), "Testing_Hours_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
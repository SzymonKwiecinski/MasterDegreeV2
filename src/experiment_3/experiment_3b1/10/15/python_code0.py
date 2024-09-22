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

# Create the linear programming problem
problem = pulp.LpProblem("Daily_Profit_Maximization", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0)  # Units produced for each product
o = pulp.LpVariable("o", lowBound=0)  # Overtime hours

# Objective function
profit_terms = [
    (data['Price'][i] * x[i] for i in range(data['N'])),
]
material_cost_terms = [
    (data['MaterialCost'][i] * x[i] for i in range(data['N'])),
]
total_material_cost = pulp.lpSum(material_cost_terms)
material_discount = (data['MaterialDiscount'] / 100) * (total_material_cost > data['DiscountThreshold'])
objective = pulp.lpSum(profit_terms) - (total_material_cost * (1 - material_discount)) - (o * data['OvertimeAssemblyCost'])

problem += objective, "Total_Profit"

# Constraints
# 1. Assembly labor constraint
problem += pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + o <= data['MaxAssembly'] + data['MaxOvertimeAssembly'], "Assembly_Labor_Constraint"

# 2. Testing labor constraint
problem += pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting'], "Testing_Labor_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
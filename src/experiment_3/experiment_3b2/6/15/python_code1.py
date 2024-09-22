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

# Model
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0, cat='Integer')
y = pulp.LpVariable("y", lowBound=0, cat='Integer')
z = pulp.LpVariable("z", cat='Binary')

# Objective Function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) - \
         pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N'])) * (1 - data['MaterialDiscount'] / 100 * z) - \
         data['OvertimeAssemblyCost'] * y

problem += profit, "Total_Profit"

# Constraints
problem += pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) <= data['MaxAssembly'] + y, "Assembly_Constraint"
problem += pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting'], "Testing_Constraint"
problem += y <= data['MaxOvertimeAssembly'], "Max_Overtime_Constraint"
problem += pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N'])) >= data['DiscountThreshold'] * z, "Material_Cost_Constraint"

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
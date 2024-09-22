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

# Problem
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat="Integer") for i in range(data['N'])]
o = pulp.LpVariable("overtime_assembly_hours", lowBound=0)

# Total material cost
total_material_cost = pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N']))

# Discount coefficient δ
delta = pulp.LpVariable("delta", lowBound=0, upBound=1, cat="Continuous")

# Objective Function
problem += pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) - (total_material_cost * (1 - delta)) - (data['OvertimeAssemblyCost'] * o)

# Constraints
problem += pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) <= data['MaxAssembly'] + o
problem += pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting']
problem += o <= data['MaxOvertimeAssembly']

# Discount threshold constraint
problem += total_material_cost <= data['DiscountThreshold'] + (data['DiscountThreshold'] * delta)
problem += total_material_cost > data['DiscountThreshold'] * (1 - delta)

# Solve
problem.solve()

# Output
daily_profit = pulp.value(problem.objective)
units_produced = [pulp.value(x[i]) for i in range(data['N'])]
overtime_assembly = pulp.value(o)
material_bought = sum(data['MaterialCost'][i] * units_produced[i] for i in range(data['N']))

print(f"Daily Profit: {daily_profit}")
print(f"Units Produced: {units_produced}")
print(f"Overtime Assembly Hours: {overtime_assembly}")
print(f"Total Material Bought Cost: {material_bought}")
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
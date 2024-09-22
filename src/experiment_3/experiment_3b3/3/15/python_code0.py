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

# Problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f"x_{i}", lowBound=0, cat='Continuous') for i in range(data['N'])]
y = pulp.LpVariable("y", lowBound=0, cat='Continuous')

# Objective Function
material_discount_factor = 1 - data['MaterialDiscount'] / 100
daily_profit = (
    pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) -
    pulp.lpSum(data['MaterialCost'][i] * x[i] * material_discount_factor for i in range(data['N'])) -
    y * data['OvertimeAssemblyCost']
)
problem += daily_profit

# Constraints
# Total assembly hours
problem += (
    pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + y <=
    data['MaxAssembly'] + data['MaxOvertimeAssembly']
)

# Total testing hours
problem += (
    pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting']
)

# Solve
problem.solve()

# Objective Value
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
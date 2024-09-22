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
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x{i}', lowBound=0, cat='Integer') for i in range(data['N'])]
y = pulp.LpVariable('y', lowBound=0, upBound=data['MaxOvertimeAssembly'], cat='Continuous')

# Constraints
problem += pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) <= data['MaxAssembly'] + y
problem += pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting']

# Material Cost Calculations
material_cost = pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N']))

# Apply discounts if applicable
material_cost_discounted = pulp.LpVariable('MaterialCostDiscounted', cat='Continuous')
problem += material_cost_discounted >= material_cost - data['DiscountThreshold'] * (1 - data['MaterialDiscount']/100)
problem += material_cost_discounted <= material_cost * (1 - data['MaterialDiscount']/100)
problem += material_cost_discounted >= material_cost

# Objective Function
profit = (
    pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) -
    data['OvertimeAssemblyCost'] * y -
    material_cost_discounted
)

problem += profit

# Solve problem
problem.solve()

# Output
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
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

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
unitsProduced = [pulp.LpVariable(f'unitsProduced_{i}', lowBound=0, cat='Integer') for i in range(data['N'])]
overtimeAssembly = pulp.LpVariable('overtimeAssembly', lowBound=0, upBound=data['MaxOvertimeAssembly'], cat='Continuous')
materialBought = pulp.LpVariable('materialBought', lowBound=0, cat='Continuous')

# Objective Function
material_cost = pulp.lpSum(data['MaterialCost'][i] * unitsProduced[i] for i in range(data['N']))
total_material_cost_discounted = pulp.lpSum(data['MaterialCost'][i] * unitsProduced[i] * (1 - data['MaterialDiscount'] / 100) for i in range(data['N'])) 
profit = pulp.lpSum(data['Price'][i] * unitsProduced[i] for i in range(data['N'])) - (
    total_material_cost_discounted * (material_cost > data['DiscountThreshold']) +
    material_cost * (material_cost <= data['DiscountThreshold']) +
    overtimeAssembly * data['OvertimeAssemblyCost']
)

problem += profit

# Constraints
problem += pulp.lpSum(data['AssemblyHour'][i] * unitsProduced[i] for i in range(data['N'])) <= data['MaxAssembly'] + overtimeAssembly
problem += pulp.lpSum(data['TestingHour'][i] * unitsProduced[i] for i in range(data['N'])) <= data['MaxTesting']

# Solve the problem
problem.solve()

# Output the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
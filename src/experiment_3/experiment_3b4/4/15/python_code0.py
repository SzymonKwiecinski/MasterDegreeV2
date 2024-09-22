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

# Initialize the problem
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Continuous') for i in range(data['N'])]
o = pulp.LpVariable('o', lowBound=0, cat='Continuous')

# Objective function
revenue = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))
material_cost = pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N']))
discounted_material_cost = (
    material_cost * (1 - data['MaterialDiscount'] / 100) if material_cost > data['DiscountThreshold'] else material_cost
)
total_cost = data['OvertimeAssemblyCost'] * o + discounted_material_cost
problem += revenue - total_cost

# Constraints
problem += pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) <= data['MaxAssembly'] + o
problem += pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting']
problem += o <= data['MaxOvertimeAssembly']

# Solve the problem
problem.solve()

# Print the results
print(f"Units Produced: {[pulp.value(x[i]) for i in range(data['N'])]}")
print(f"Overtime Assembly: {pulp.value(o)}")
if material_cost > data['DiscountThreshold']:
    print(f"Material Cost After Discount: {pulp.value(discounted_material_cost)}")
else:
    print(f"Material Cost: {pulp.value(material_cost)}")
print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
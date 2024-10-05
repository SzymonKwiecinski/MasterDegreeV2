import pulp

# Load data
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

# Decision Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0, cat='Integer') for i in range(data['N'])]
o = pulp.LpVariable('o', lowBound=0, cat='Continuous')

# Problem
problem = pulp.LpProblem('Daily_Profit_Maximization', pulp.LpMaximize)

# Objective Function
total_price = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))
total_material_cost = pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N']))
discount = data['MaterialDiscount'] / 100 if total_material_cost > data['DiscountThreshold'] else 0
problem += total_price - total_material_cost * (1 - discount) - data['OvertimeAssemblyCost'] * o

# Constraints
problem += pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) <= data['MaxAssembly'] + o
problem += pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting']
problem += o <= data['MaxOvertimeAssembly']

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
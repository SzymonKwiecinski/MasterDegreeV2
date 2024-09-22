import pulp
import json

# Data in JSON format
data = json.loads("{'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}")

# Parameters
N = data['N']
assembly_hours = data['AssemblyHour']
testing_hours = data['TestingHour']
material_cost = data['MaterialCost']
max_assembly = data['MaxAssembly']
max_testing = data['MaxTesting']
price = data['Price']
max_overtime_assembly = data['MaxOvertimeAssembly']
overtime_assembly_cost = data['OvertimeAssemblyCost']
material_discount = data['MaterialDiscount']
discount_threshold = data['DiscountThreshold']

# Decision Variables
x = pulp.LpVariable.dicts("units_produced", range(N), lowBound=0, cat='Continuous')
y = pulp.LpVariable("overtime_assembly", lowBound=0, cat='Continuous')

# Problem Definition
problem = pulp.LpProblem("Daily_Profit_Maximization", pulp.LpMaximize)

# Objective Function
material_cost_total = pulp.lpSum(material_cost[i] * x[i] for i in range(N))

# Discount term based on material costs
d = pulp.LpVariable("discount", lowBound=0, cat='Continuous')
problem += pulp.lpSum(price[i] * x[i] for i in range(N)) - (material_cost_total - d + overtime_assembly_cost * y)

# Constraints
problem += pulp.lpSum(assembly_hours[i] * x[i] for i in range(N)) + y <= max_assembly + max_overtime_assembly
problem += pulp.lpSum(testing_hours[i] * x[i] for i in range(N)) <= max_testing
problem += y <= max_overtime_assembly

# Material discount condition
problem += material_cost_total <= discount_threshold + (1 - d/material_cost_total) * (1 - material_discount / 100) * material_cost_total

# Solve the problem
problem.solve()

# Output results
units_produced = {i: x[i].varValue for i in range(N)}
overtime_hours = y.varValue
material_bought = material_cost_total.varValue

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Units Produced: {units_produced}')
print(f'Overtime Assembly Hours: {overtime_hours}')
print(f'Total Material Bought: {material_bought}')
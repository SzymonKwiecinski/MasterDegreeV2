import pulp
import json

# Input data in JSON format
data = json.loads("{'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}")

# Extracting data
N = data['N']
assemblyHour = data['AssemblyHour']
testingHour = data['TestingHour']
materialCost = data['MaterialCost']
maxAssembly = data['MaxAssembly']
maxTesting = data['MaxTesting']
price = data['Price']
maxOvertimeAssembly = data['MaxOvertimeAssembly']
overtimeAssemblyCost = data['OvertimeAssemblyCost']
materialDiscount = data['MaterialDiscount']
discountThreshold = data['DiscountThreshold']

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("units_produced", range(N), lowBound=0, cat='Continuous')
o = pulp.LpVariable("overtime_hours", lowBound=0, cat='Continuous')

# Objective function
discount_expr = pulp.lpSum([materialCost[i] * x[i] for i in range(N)]) * (materialDiscount / 100)
total_material_cost = pulp.lpSum([materialCost[i] * x[i] for i in range(N)])

problem += pulp.lpSum([price[i] * x[i] for i in range(N)]) - (total_material_cost - pulp.lpMax(0, discount_expr)) - (o * overtimeAssemblyCost), "Total_Profit"

# Constraints
# 1. Assembly labor constraint
problem += pulp.lpSum([assemblyHour[i] * x[i] for i in range(N)]) + o <= maxAssembly + maxOvertimeAssembly, "Assembly_Labor_Constraint"

# 2. Testing labor constraint
problem += pulp.lpSum([testingHour[i] * x[i] for i in range(N)]) <= maxTesting, "Testing_Labor_Constraint"

# 3. Material bought
m = total_material_cost
problem += m == pulp.lpSum([materialCost[i] * x[i] for i in range(N)]), "Material_Bought"

# 4. Overtime constraint
problem += o <= maxOvertimeAssembly, "Overtime_Constraint"

# Solve the problem
problem.solve()

# Output results
units_produced = [pulp.value(x[i]) for i in range(N)]
overtime_hours = pulp.value(o)
material_bought = pulp.value(m)
daily_profit = pulp.value(problem.objective)

# Print results
print(f'(Objective Value): <OBJ>{daily_profit}</OBJ>')
print(f'Units Produced: {units_produced}')
print(f'Overtime Scheduled: {overtime_hours}')
print(f'Material Bought: {material_bought}')
import pulp
import json

# Data input
data = json.loads("{'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}")

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(1, data['N'] + 1), lowBound=0, cat='Integer')
y = pulp.LpVariable("y", lowBound=0, cat='Integer')

# Parameters
assembly_hour = data['AssemblyHour']
testing_hour = data['TestingHour']
material_cost = data['MaterialCost']
price = data['Price']
max_assembly = data['MaxAssembly']
max_testing = data['MaxTesting']
max_overtime_assembly = data['MaxOvertimeAssembly']
overtime_assembly_cost = data['OvertimeAssemblyCost']
material_discount = data['MaterialDiscount'] / 100
discount_threshold = data['DiscountThreshold']

# Objective Function
profit_terms = []
for i in range(1, data['N'] + 1):
    profit_terms.append(price[i - 1] * x[i])
    
material_cost_terms = []
for i in range(1, data['N'] + 1):
    material_cost_terms.append(material_cost[i - 1] * x[i] * (1 - pulp.LpVariable("discount", lowBound=0, cat='Binary')))

# Discount condition
discount_condition = pulp.lpSum(material_cost[i - 1] * x[i] for i in range(1, data['N'] + 1)) > discount_threshold

# Objective function
problem += pulp.lpSum(profit_terms) - pulp.lpSum(material_cost_terms) - (overtime_assembly_cost * y), "Total_Profit"

# Constraints
problem += pulp.lpSum(assembly_hour[i - 1] * x[i] for i in range(1, data['N'] + 1)) <= max_assembly + y, "Assembly_Hours_Constraint"
problem += pulp.lpSum(testing_hour[i - 1] * x[i] for i in range(1, data['N'] + 1)) <= max_testing, "Testing_Hours_Constraint"
problem += y <= max_overtime_assembly, "Max_Overtime_Assembly_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
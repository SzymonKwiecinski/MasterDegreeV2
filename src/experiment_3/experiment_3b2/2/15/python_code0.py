import pulp
import json

# Data provided in JSON format
data = json.loads("{'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}")

N = data['N']
assembly_hours = data['AssemblyHour']
testing_hours = data['TestingHour']
material_costs = data['MaterialCost']
max_assembly = data['MaxAssembly']
max_testing = data['MaxTesting']
prices = data['Price']
max_overtime_assembly = data['MaxOvertimeAssembly']
overtime_assembly_cost = data['OvertimeAssemblyCost']
material_discount = data['MaterialDiscount']
discount_threshold = data['DiscountThreshold']

# Initialize the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat='Integer')
y = pulp.LpVariable("y", lowBound=0, upBound=max_overtime_assembly, cat='Integer')

# Discount calculation
material_cost_sum = pulp.lpSum([material_costs[i] * x[i] for i in range(N)])
discount = pulp.LpVariable("d", lowBound=0, cat='Continuous')
problem += pulp.lpSum([material_costs[i] * x[i] for i in range(N)]) <= discount_threshold, "DiscountCondition1"
problem += discount == 0, "NoDiscount"

problem += pulp.lpSum([material_costs[i] * x[i] for i in range(N)]) > discount_threshold, "DiscountCondition2"
problem += discount == (material_discount / 100), "ApplyDiscount"

# Objective Function
profit_expr = pulp.lpSum([prices[i] * x[i] for i in range(N)]) - (pulp.lpSum([material_costs[i] * x[i] * (1 - discount) for i in range(N)]) + y * overtime_assembly_cost)
problem += profit_expr, "Total_Profit"

# Constraints
problem += pulp.lpSum([assembly_hours[i] * x[i] for i in range(N)]) <= max_assembly + y, "AssemblyConstraint"
problem += pulp.lpSum([testing_hours[i] * x[i] for i in range(N)]) <= max_testing, "TestingConstraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
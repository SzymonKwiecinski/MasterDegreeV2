import pulp
import json

# Extract data from JSON
data = json.loads('{"N": 2, "AssemblyHour": [0.25, 0.3333], "TestingHour": [0.125, 0.3333], "MaterialCost": [1.2, 0.9], "MaxAssembly": 10, "MaxTesting": 70, "Price": [9, 8], "MaxOvertimeAssembly": 50, "OvertimeAssemblyCost": 5, "MaterialDiscount": 10, "DiscountThreshold": 300}')

# Parameters
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

# Create the problem
problem = pulp.LpProblem("Daily_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat='Continuous')  # number of units produced
y = pulp.LpVariable("y", lowBound=0, cat='Continuous')  # overtime hours

# Objective Function
profit_expr = pulp.lpSum(prices[i] * x[i] for i in range(N)) \
              - pulp.lpSum(material_costs[i] * x[i] for i in range(N)) \
              - overtime_assembly_cost * y \
              - material_discount * pulp.lpSum(material_costs[i] * x[i] for i in range(N)) >= discount_threshold

problem += pulp.lpSum(prices[i] * x[i] for i in range(N)) \
           - pulp.lpSum(material_costs[i] * x[i] for i in range(N)) \
           - overtime_assembly_cost * y, "Total_Profit"

# Constraints
problem += pulp.lpSum(assembly_hours[i] * x[i] for i in range(N)) + y <= max_assembly + max_overtime_assembly, "Assembly_Labor_Constraint"
problem += pulp.lpSum(testing_hours[i] * x[i] for i in range(N)) <= max_testing, "Testing_Labor_Constraint"

# Solve the problem
problem.solve()

# Output results
units_produced = [x[i].varValue for i in range(N)]
overtime_hours = y.varValue
material_bought = sum(material_costs[i] * x[i].varValue for i in range(N))

print(f'Units Produced: {units_produced}')
print(f'Overtime Assembly Hours: {overtime_hours}')
print(f'Material Bought: {material_bought}')
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
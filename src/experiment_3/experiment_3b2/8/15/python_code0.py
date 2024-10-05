import pulp
import json

# Data input
data_json = '''{
    "N": 2,
    "AssemblyHour": [0.25, 0.3333],
    "TestingHour": [0.125, 0.3333],
    "MaterialCost": [1.2, 0.9],
    "MaxAssembly": 10,
    "MaxTesting": 70,
    "Price": [9, 8],
    "MaxOvertimeAssembly": 50,
    "OvertimeAssemblyCost": 5,
    "MaterialDiscount": 10,
    "DiscountThreshold": 300
}'''

data = json.loads(data_json)

# Model
problem = pulp.LpProblem("Profit_Maximization", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("Product", range(data['N']), lowBound=0, cat='Integer')
y = pulp.LpVariable("OvertimeAssembly", lowBound=0, upBound=data['MaxOvertimeAssembly'], cat='Continuous')

# Objective Function
material_cost = pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N']))
revenue = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N']))
total_material_cost = material_cost

# Applying discount if applicable
discount_condition = material_cost > data['DiscountThreshold']
if_expr = (1 - data['MaterialDiscount'] / 100) * material_cost
total_cost = pulp.lpSum([material_cost * (1 if not discount_condition else 0), if_expr * (1 if discount_condition else 0)])

problem += revenue - (total_cost + data['OvertimeAssemblyCost'] * y), "Total_Profit"

# Constraints
problem += pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) <= data['MaxAssembly'] + y, "Assembly_Labor_Constraint"
problem += pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting'], "Testing_Labor_Constraint"

# Solve
problem.solve()

# Output results
print(f'(Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
units_produced = {i: x[i].varValue for i in range(data['N'])}
print(f'Units Produced: {units_produced}')
print(f'Overtime Assembly: {y.varValue}')
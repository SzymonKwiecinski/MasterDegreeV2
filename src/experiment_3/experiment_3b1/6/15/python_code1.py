import pulp
import json

data = json.loads('{"N": 2, "AssemblyHour": [0.25, 0.3333], "TestingHour": [0.125, 0.3333], "MaterialCost": [1.2, 0.9], "MaxAssembly": 10, "MaxTesting": 70, "Price": [9, 8], "MaxOvertimeAssembly": 50, "OvertimeAssemblyCost": 5, "MaterialDiscount": 10, "DiscountThreshold": 300}')

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

# Problem Definition
problem = pulp.LpProblem("Company_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat='Integer')
overtime_assembly = pulp.LpVariable("overtimeAssembly", lowBound=0)

# Objective Function
profit = pulp.lpSum([price[i] * x[i] for i in range(N)]) - (
    pulp.lpSum([material_cost[i] * x[i] for i in range(N)]) * 
    (1 - (material_discount / 100) * pulp.lpSum([
        1 if pulp.lpSum([material_cost[i] * x[i] for i in range(N)]) > discount_threshold else 0
        for i in range(N)
    ]) > 0) +
    overtime_assembly_cost * overtime_assembly
)
problem += profit

# Constraints
problem += pulp.lpSum([assembly_hours[i] * x[i] for i in range(N)]) + overtime_assembly <= max_assembly + max_overtime_assembly, "AssemblyTimeConstraint"
problem += pulp.lpSum([testing_hours[i] * x[i] for i in range(N)]) <= max_testing, "TestingTimeConstraint"

# Solve the Problem
problem.solve()

# Output the results
units_produced = [x[i].varValue for i in range(N)]
material_bought = sum(material_cost[i] * x[i].varValue for i in range(N))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Units Produced: {units_produced}')
print(f'Overtime Assembly: {overtime_assembly.varValue}')
print(f'Material Bought: {material_bought}')
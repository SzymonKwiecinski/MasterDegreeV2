import pulp
import json

# Data input in JSON format
data = json.loads('{"N": 2, "AssemblyHour": [0.25, 0.3333], "TestingHour": [0.125, 0.3333], "MaterialCost": [1.2, 0.9], "MaxAssembly": 10, "MaxTesting": 70, "Price": [9, 8], "MaxOvertimeAssembly": 50, "OvertimeAssemblyCost": 5, "MaterialDiscount": 10, "DiscountThreshold": 300}')

# Parameters
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

# Decision Variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat='Continuous')  # Units of product
y = pulp.LpVariable("y", lowBound=0, cat='Continuous')  # Overtime hours

# Problem
problem = pulp.LpProblem("Production_Problem", pulp.LpMaximize)

# Objective Function
discount_expr = pulp.lpSum(materialCost[i] * x[i] for i in range(N)) > discountThreshold

# Set the objective
problem += (pulp.lpSum(price[i] * x[i] for i in range(N)) - 
             (pulp.lpSum(materialCost[i] * x[i] for i in range(N)) + 
              overtimeAssemblyCost * y - 
              pulp.lpSum((materialDiscount / 100.0) * materialCost[i] * x[i] for i in range(N) if discount_expr)))

# Constraints
problem += (pulp.lpSum(assemblyHour[i] * x[i] for i in range(N)) + y <= maxAssembly + maxOvertimeAssembly, "Assembly_Hours_Constraint")
problem += (pulp.lpSum(testingHour[i] * x[i] for i in range(N)) <= maxTesting, "Testing_Hours_Constraint")
problem += (y <= maxOvertimeAssembly, "Max_Overtime_Assembly")

# Solve the problem
problem.solve()

# Output the result
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
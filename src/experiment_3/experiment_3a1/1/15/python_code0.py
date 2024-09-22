import pulp
import json

# Data in JSON format
data = json.loads('{"N": 2, "AssemblyHour": [0.25, 0.3333], "TestingHour": [0.125, 0.3333], "MaterialCost": [1.2, 0.9], "MaxAssembly": 10, "MaxTesting": 70, "Price": [9, 8], "MaxOvertimeAssembly": 50, "OvertimeAssemblyCost": 5, "MaterialDiscount": 10, "DiscountThreshold": 300}')

# Model
problem = pulp.LpProblem("Production_Problem", pulp.LpMaximize)

# Variables
x = [pulp.LpVariable(f'x_{i}', lowBound=0) for i in range(data['N'])]
overtimeAssembly = pulp.LpVariable("overtimeAssembly", lowBound=0)
materialBought = pulp.LpVariable("materialBought", lowBound=0)

# Objective Function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) - materialBought - (overtimeAssembly * data['OvertimeAssemblyCost'])
problem += profit

# Constraints
problem += (pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + overtimeAssembly <= data['MaxAssembly'] + data['MaxOvertimeAssembly'], "Assembly_Hours_Constraint")
problem += (pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting'], "Testing_Hours_Constraint")
problem += (materialBought == pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N'])), "Material_Cost_Calculation")

# Discount constraint
discounted_material = materialBought * (1 - data['MaterialDiscount'] / 100)
problem += (pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(data['N'])) <= data['DiscountThreshold'], "No_Discount") \
           | (materialBought == discounted_material, "With_Discount")

# Solve the problem
problem.solve()

# Print the objective value and results
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
print(f'Units Produced: {[pulp.value(x[i]) for i in range(data["N"])]}')
print(f'Overtime Assembly: {pulp.value(overtimeAssembly)}')
print(f'Material Bought: {pulp.value(materialBought)}')
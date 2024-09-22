import pulp
import json

# Data provided
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

# Create a Linear Programming problem
problem = pulp.LpProblem("Production_Optimization", pulp.LpMaximize)

# Decision Variables
unitsProduced = [pulp.LpVariable(f'unitsProduced_{i+1}', lowBound=0, cat='Continuous') for i in range(data['N'])]
overtimeAssembly = pulp.LpVariable('overtimeAssembly', lowBound=0, cat='Continuous')
materialBought = pulp.LpVariable('materialBought', lowBound=0, cat='Continuous')

# Objective Function
total_revenue = pulp.lpSum(data['Price'][i] * unitsProduced[i] for i in range(data['N']))
total_material_cost = pulp.lpSum(data['MaterialCost'][i] * unitsProduced[i] for i in range(data['N']))
material_cost_after_discount = (total_material_cost * (1 - data['MaterialDiscount'] / 100) 
                                 if total_material_cost > data['DiscountThreshold'] 
                                 else total_material_cost)

total_cost = material_cost_after_discount + (data['OvertimeAssemblyCost'] * overtimeAssembly)

problem += total_revenue - total_cost, "Total_Profit"

# Constraints
problem += (pulp.lpSum(data['AssemblyHour'][i] * unitsProduced[i] for i in range(data['N'])) 
             + overtimeAssembly <= data['MaxAssembly'] + data['MaxOvertimeAssembly'], 
             "Assembly_Labor_Constraint")

problem += (pulp.lpSum(data['TestingHour'][i] * unitsProduced[i] for i in range(data['N'])) 
             <= data['MaxTesting'], 
             "Testing_Labor_Constraint")

# Solve the problem
problem.solve()

# Output results
daily_profit = pulp.value(problem.objective)
units_produced_values = [pulp.value(unitsProduced[i]) for i in range(data['N'])]
print(f' (Objective Value): <OBJ>{daily_profit}</OBJ>')
print(f'Units Produced: {units_produced_values}')
print(f'Overtime Assembly: {pulp.value(overtimeAssembly)}')
print(f'Material Bought: {pulp.value(materialBought)}')
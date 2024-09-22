import json
import pulp

# Input data
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

# Variables
N = data['N']
assembly_hours = data['AssemblyHour']
testing_hours = data['TestingHour']
material_costs = data['MaterialCost']
max_assembly = data['MaxAssembly']
max_testing = data['MaxTesting']
prices = data['Price']
max_overtime_assembly = data['MaxOvertimeAssembly']
overtime_assembly_cost = data['OvertimeAssemblyCost']
material_discount = data['MaterialDiscount'] / 100
discount_threshold = data['DiscountThreshold']

# Problem definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
units_produced = [pulp.LpVariable(f'units_produced_{i}', lowBound=0, cat='Integer') for i in range(N)]
overtime_assembly = pulp.LpVariable('overtime_assembly', lowBound=0, cat='Continuous')

# Objective function (Profit)
revenue = sum(prices[i] * units_produced[i] for i in range(N))
cost_material = sum(material_costs[i] * units_produced[i] for i in range(N))
total_material_cost = cost_material * (1 - material_discount) if cost_material > discount_threshold else cost_material
cost_assembly = sum(assembly_hours[i] * units_produced[i] for i in range(N))
cost_testing = sum(testing_hours[i] * units_produced[i] for i in range(N))
total_cost = total_material_cost + cost_assembly + cost_testing + overtime_assembly * overtime_assembly_cost

problem += revenue - total_cost, "Total_Profit"

# Constraints
problem += sum(assembly_hours[i] * units_produced[i] for i in range(N)) + overtime_assembly <= max_assembly + max_overtime_assembly, "Assembly_Constraint"
problem += sum(testing_hours[i] * units_produced[i] for i in range(N)) <= max_testing, "Testing_Constraint"

# Solve the problem
problem.solve()

# Output the results
daily_profit = pulp.value(problem.objective)
units_produced_values = [pulp.value(units_produced[i]) for i in range(N)]
overtime_assembly_value = pulp.value(overtime_assembly)
material_bought = sum(material_costs[i] * units_produced_values[i] for i in range(N))

# Format the output
result = {
    "dailyProfit": daily_profit,
    "unitsProduced": units_produced_values,
    "overtimeAssembly": overtime_assembly_value,
    "materialBought": material_bought
}

# Print the objective value
print(f' (Objective Value): <OBJ>{daily_profit}</OBJ>')
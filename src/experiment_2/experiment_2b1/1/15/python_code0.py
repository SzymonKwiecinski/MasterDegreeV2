import pulp
import json

# Input Data
data = {'N': 2, 
        'AssemblyHour': [0.25, 0.3333], 
        'TestingHour': [0.125, 0.3333], 
        'MaterialCost': [1.2, 0.9], 
        'MaxAssembly': 10, 
        'MaxTesting': 70, 
        'Price': [9, 8], 
        'MaxOvertimeAssembly': 50, 
        'OvertimeAssemblyCost': 5, 
        'MaterialDiscount': 10, 
        'DiscountThreshold': 300}

N = data['N']
assembly_hour = data['AssemblyHour']
testing_hour = data['TestingHour']
material_cost = data['MaterialCost']
max_assembly = data['MaxAssembly']
max_testing = data['MaxTesting']
price = data['Price']
max_overtime_assembly = data['MaxOvertimeAssembly']
overtime_assembly_cost = data['OvertimeAssemblyCost']
material_discount = data['MaterialDiscount'] / 100
discount_threshold = data['DiscountThreshold']

# Problem Definition
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
units_produced = [pulp.LpVariable(f'unitsProduced_{i}', lowBound=0, cat='Integer') for i in range(N)]
overtime_assembly = pulp.LpVariable('overtimeAssembly', lowBound=0, upBound=max_overtime_assembly)

# Objective Function
revenue = pulp.lpSum([units_produced[i] * price[i] for i in range(N)])
material_costs = pulp.lpSum([
    units_produced[i] * material_cost[i] for i in range(N)
])
overtime_cost = overtime_assembly * overtime_assembly_cost

# Total cost considering discount
total_material_cost = material_costs * (1 - material_discount) if material_costs > discount_threshold else material_costs

daily_profit = revenue - (total_material_cost + overtime_cost)

problem += daily_profit

# Constraints
problem += pulp.lpSum([units_produced[i] * assembly_hour[i] for i in range(N)]) + overtime_assembly <= max_assembly
problem += pulp.lpSum([units_produced[i] * testing_hour[i] for i in range(N)]) <= max_testing

# Solve the problem
problem.solve()

# Output
daily_profit_value = pulp.value(problem.objective)
units_produced_values = [pulp.value(units_produced[i]) for i in range(N)]
overtime_assembly_value = pulp.value(overtime_assembly)
material_bought_value = sum([units_produced_values[i] * material_cost[i] for i in range(N)])

output = {
    "dailyProfit": daily_profit_value,
    "unitsProduced": units_produced_values,
    "overtimeAssembly": overtime_assembly_value,
    "materialBought": material_bought_value
}

print(f' (Objective Value): <OBJ>{daily_profit_value}</OBJ>')
import json
import pulp

data = {'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 
        'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70,
        'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 
        'MaterialDiscount': 10, 'DiscountThreshold': 300}

# Extracting data
N = data['N']
assembly_hour = data['AssemblyHour']
testing_hour = data['TestingHour']
material_cost = data['MaterialCost']
max_assembly = data['MaxAssembly']
max_testing = data['MaxTesting']
price = data['Price']
max_overtime_assembly = data['MaxOvertimeAssembly']
overtime_assembly_cost = data['OvertimeAssemblyCost']
material_discount = data['MaterialDiscount']
discount_threshold = data['DiscountThreshold']

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
units_produced = [pulp.LpVariable(f'Units_Produced_{i}', lowBound=0, cat='Integer') for i in range(N)]
overtime_assembly = pulp.LpVariable('Overtime_Assembly', lowBound=0, upBound=max_overtime_assembly)

# Objective function: Maximize profit
total_revenue = pulp.lpSum([price[i] * units_produced[i] for i in range(N)])
total_material_cost = pulp.lpSum([material_cost[i] * units_produced[i] for i in range(N)])
total_assembly_hours = pulp.lpSum([assembly_hour[i] * units_produced[i] for i in range(N)]) + overtime_assembly
total_testing_hours = pulp.lpSum([testing_hour[i] * units_produced[i] for i in range(N)])

# Discount calculation
total_material_cost_with_discount = total_material_cost
if total_material_cost > discount_threshold:
    total_material_cost_with_discount = total_material_cost * (1 - material_discount / 100)

total_overtime_cost = overtime_assembly * overtime_assembly_cost

# Daily profit
daily_profit = total_revenue - (total_material_cost_with_discount + total_overtime_cost)

# Adding objective to the problem
problem += daily_profit

# Constraints
problem += total_assembly_hours <= max_assembly + max_overtime_assembly
problem += total_testing_hours <= max_testing

# Solve the problem
problem.solve()

# Output results
units_produced_result = [int(units_produced[i].varValue) for i in range(N)]
total_material_bought = sum(material_cost[i] * units_produced_result[i] for i in range(N))

daily_profit_value = pulp.value(problem.objective)

output = {
    "dailyProfit": daily_profit_value,
    "unitsProduced": units_produced_result,
    "overtimeAssembly": overtime_assembly.varValue,
    "materialBought": total_material_bought
}

# Printing the results
print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{daily_profit_value}</OBJ>')
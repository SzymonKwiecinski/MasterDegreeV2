import pulp
import json

# Data input
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
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
units_produced = [pulp.LpVariable(f'Units_Produced_{i}', lowBound=0, cat='Integer') for i in range(N)]
overtime_assembly = pulp.LpVariable('Overtime_Assembly', lowBound=0, cat='Continuous')

# Constraints
problem += pulp.lpSum([assembly_hours[i] * units_produced[i] for i in range(N)]) + overtime_assembly <= max_assembly + max_overtime_assembly, "Assembly_Hours_Constraint"
problem += pulp.lpSum([testing_hours[i] * units_produced[i] for i in range(N)]) <= max_testing, "Testing_Hours_Constraint"

# Objective function
total_revenue = pulp.lpSum([prices[i] * units_produced[i] for i in range(N)])
total_material_cost = pulp.lpSum([material_costs[i] * units_produced[i] for i in range(N)])

# Apply material discount if applicable
total_material_cost_discounted = total_material_cost * (1 - (material_discount / 100) * (total_material_cost >= discount_threshold))

# Total cost
total_cost = total_material_cost_discounted + (overtime_assembly * overtime_assembly_cost)

# Daily profit
daily_profit = total_revenue - total_cost

# Set the objective
problem += daily_profit, "Objective"

# Solve the problem
problem.solve()

# Output the results
daily_profit_value = pulp.value(problem.objective)
units_produced_values = [pulp.value(var) for var in units_produced]
overtime_assembly_value = pulp.value(overtime_assembly)
total_material_bought = pulp.value(total_material_cost)

output = {
    "dailyProfit": daily_profit_value,
    "unitsProduced": units_produced_values,
    "overtimeAssembly": overtime_assembly_value,
    "materialBought": total_material_bought
}

print(json.dumps(output))
print(f' (Objective Value): <OBJ>{daily_profit_value}</OBJ>')
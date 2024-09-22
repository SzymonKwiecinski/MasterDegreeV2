import pulp
import json

# Input data in JSON format
data = {'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 
        'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 
        'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}

# Extracting data
N = data['N']
assembly_hours = data['AssemblyHour']
testing_hours = data['TestingHour']
material_costs = data['MaterialCost']
max_assembly = data['MaxAssembly']
max_testing = data['MaxTesting']
prices = data['Price']
max_overtime_assembly = data['MaxOvertimeAssembly']
overtime_assembly_cost = data['OvertimeAssemblyCost']
material_discount = data['MaterialDiscount']/100
discount_threshold = data['DiscountThreshold']

# Creating the optimization problem
problem = pulp.LpProblem("MaximizeDailyProfit", pulp.LpMaximize)

# Decision variables
units_produced = [pulp.LpVariable(f'units_produced_{i}', lowBound=0, cat='Integer') for i in range(N)]
overtime_assembly = pulp.LpVariable('overtime_assembly', lowBound=0, upBound=max_overtime_assembly)
material_bought = pulp.LpVariable('material_bought', lowBound=0)

# Objective function
total_revenue = pulp.lpSum([units_produced[i] * prices[i] for i in range(N)])
total_material_cost = pulp.lpSum([units_produced[i] * material_costs[i] for i in range(N)])
if material_bought >= discount_threshold:
    total_material_cost *= (1 - material_discount)

total_assembly_hours = pulp.lpSum([units_produced[i] * assembly_hours[i] for i in range(N)])
total_testing_hours = pulp.lpSum([units_produced[i] * testing_hours[i] for i in range(N)])

# Total cost
total_cost = total_material_cost + overtime_assembly * overtime_assembly_cost
daily_profit = total_revenue - total_cost

# Constraints
problem += (total_assembly_hours + overtime_assembly <= max_assembly, "MaxAssemblyConstraint")
problem += (total_testing_hours <= max_testing, "MaxTestingConstraint")

# Set the objective
problem += daily_profit

# Solve the problem
problem.solve()

# Output results
output = {
    "dailyProfit": pulp.value(problem.objective),
    "unitsProduced": [pulp.value(units_produced[i]) for i in range(N)],
    "overtimeAssembly": pulp.value(overtime_assembly),
    "materialBought": pulp.value(material_bought)
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp
import json

# Input data
data = {'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 
        'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 
        'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 
        'MaterialDiscount': 10, 'DiscountThreshold': 300}

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
material_discount = data['MaterialDiscount']
discount_threshold = data['DiscountThreshold']

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
units_produced = [pulp.LpVariable(f'units_produced_{i}', lowBound=0, cat='Integer') for i in range(N)]
overtime_assembly = pulp.LpVariable('overtime_assembly', lowBound=0, upBound=max_overtime_assembly)

# Total assembly hours used
total_assembly_hours = pulp.lpSum([units_produced[i] * assembly_hours[i] for i in range(N)]) + overtime_assembly

# Total testing hours used
total_testing_hours = pulp.lpSum([units_produced[i] * testing_hours[i] for i in range(N)])

# Total material cost
total_material_cost = pulp.lpSum([units_produced[i] * material_costs[i] for i in range(N)])

# Revenue
total_revenue = pulp.lpSum([units_produced[i] * prices[i] for i in range(N)])

# Apply discounts if applicable
total_cost = total_material_cost
if total_material_cost >= discount_threshold:
    total_cost *= (1 - material_discount / 100)

# Objective Function
total_profit = total_revenue - (total_cost + overtime_assembly_cost * overtime_assembly)
problem += total_profit, "Total_Profit"

# Constraints
problem += total_assembly_hours <= max_assembly + overtime_assembly, "Assembly_Hours_Constraint"
problem += total_testing_hours <= max_testing, "Testing_Hours_Constraint"

# Solve the problem
problem.solve()

# Gather results
daily_profit = pulp.value(total_profit)
units_produced_values = [pulp.value(units_produced[i]) for i in range(N)]
overtime_assembly_value = pulp.value(overtime_assembly)
material_bought = sum(units_produced_values[i] * material_costs[i] for i in range(N))

# Print output
output = {
    "dailyProfit": daily_profit,
    "unitsProduced": units_produced_values,
    "overtimeAssembly": overtime_assembly_value,
    "materialBought": material_bought
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
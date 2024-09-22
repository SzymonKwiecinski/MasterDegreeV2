import pulp
import json

data = {'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 
        'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 
        'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 
        'MaterialDiscount': 10, 'DiscountThreshold': 300}

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

# Create the LP problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables for units produced
units_produced = [pulp.LpVariable(f'units_{i}', lowBound=0, cat='Integer') for i in range(N)]

# Decision variable for overtime hours
overtime_assembly = pulp.LpVariable('overtime_assembly', lowBound=0, upBound=max_overtime_assembly)

# Objective function: Maximize profit
revenue = pulp.lpSum([price[i] * units_produced[i] for i in range(N)])
total_material_cost = pulp.lpSum([material_cost[i] * units_produced[i] for i in range(N)])
total_testing_cost = pulp.lpSum([testing_hour[i] * units_produced[i] for i in range(N)]) * 0  # 0 is a placeholder for no cost mention
total_assembly_cost = pulp.lpSum([assembly_hour[i] * units_produced[i] for i in range(N)]) + overtime_assembly * overtime_assembly_cost
total_cost = total_material_cost + total_testing_cost + total_assembly_cost

# Add constraints
problem += pulp.lpSum([assembly_hour[i] * units_produced[i] for i in range(N)]) + overtime_assembly <= max_assembly
problem += pulp.lpSum([testing_hour[i] * units_produced[i] for i in range(N)]) <= max_testing

# Handle material discount if applicable
total_material_cost_with_discount = total_material_cost * (1 - material_discount) if total_material_cost >= discount_threshold else total_material_cost

# Set the objective
problem += revenue - total_material_cost_with_discount - total_assembly_cost, "Profit"

# Solve the problem
problem.solve()

# Collect the results
daily_profit = pulp.value(problem.objective)
units_produced_result = [pulp.value(units_produced[i]) for i in range(N)]
overtime_assembly_result = pulp.value(overtime_assembly)
material_bought = pulp.value(total_material_cost)

# Format output
output = {
    "dailyProfit": daily_profit,
    "unitsProduced": units_produced_result,
    "overtimeAssembly": overtime_assembly_result,
    "materialBought": material_bought
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
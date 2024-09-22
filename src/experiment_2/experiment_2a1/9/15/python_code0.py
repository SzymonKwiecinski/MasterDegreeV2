import pulp
import json

# Input data
data = {'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 
        'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 
        'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}

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

# Define the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
units_produced = [pulp.LpVariable(f'UnitsProduced_{i}', lowBound=0, cat='Integer') for i in range(N)]
overtime_assembly = pulp.LpVariable('OvertimeAssembly', lowBound=0, upBound=max_overtime_assembly)

# Objective Function
revenue = pulp.lpSum([price[i] * units_produced[i] for i in range(N)])
cost_of_materials = pulp.lpSum([material_cost[i] * units_produced[i] for i in range(N)])

# Check if the total material cost exceeds the discount threshold to apply discount
total_material_cost = cost_of_materials * (1 - material_discount / 100) if cost_of_materials >= discount_threshold else cost_of_materials

cost_of_labor = pulp.lpSum([assembly_hour[i] * units_produced[i] for i in range(N)]) + overtime_assembly * overtime_assembly_cost

total_cost = total_material_cost + cost_of_labor
profit = revenue - total_cost

problem += profit

# Constraints
problem += pulp.lpSum([assembly_hour[i] * units_produced[i] for i in range(N)]) + overtime_assembly <= max_assembly
problem += pulp.lpSum([testing_hour[i] * units_produced[i] for i in range(N)]) <= max_testing

# Solve the problem
problem.solve()

# Output the results
daily_profit = pulp.value(problem.objective)
units_produced_result = [pulp.value(units_produced[i]) for i in range(N)]
overtime_assembly_result = pulp.value(overtime_assembly)
material_bought = sum(pulp.value(units_produced[i]) * material_cost[i] for i in range(N))

# Print the objective value
print(f' (Objective Value): <OBJ>{daily_profit}</OBJ>')

# Format the output as required
output = {
    "dailyProfit": daily_profit,
    "unitsProduced": units_produced_result,
    "overtimeAssembly": overtime_assembly_result,
    "materialBought": material_bought
}

# Output the results
print(json.dumps(output))
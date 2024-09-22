import pulp

# Load data
data = {'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}

# Extracting variables from data
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
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

# Variables
units_produced = [pulp.LpVariable(f"Units_Produced_{i}", lowBound=0, cat='Integer') for i in range(N)]
overtime_assembly = pulp.LpVariable("Overtime_Assembly", lowBound=0, cat='Continuous')

# Objective Function
revenue = pulp.lpSum([price[i] * units_produced[i] for i in range(N)])
material_bought = pulp.lpSum([material_cost[i] * units_produced[i] for i in range(N)])
material_cost_total = material_bought * ((100 - material_discount) / 100 if material_bought > discount_threshold else 1)
overtime_cost = overtime_assembly * overtime_assembly_cost
total_profit = revenue - material_cost_total - overtime_cost
problem += total_profit

# Constraints
problem += pulp.lpSum([assembly_hour[i] * units_produced[i] for i in range(N)]) <= max_assembly + overtime_assembly, "Assembly_Labor_Limit"
problem += pulp.lpSum([testing_hour[i] * units_produced[i] for i in range(N)]) <= max_testing, "Testing_Labor_Limit"
problem += overtime_assembly <= max_overtime_assembly, "Overtime_Limit"

# Solve the problem
problem.solve()

# Output results
daily_profit = pulp.value(total_profit)
units_produced_vals = [pulp.value(units_produced[i]) for i in range(N)]
overtime_assembly_val = pulp.value(overtime_assembly)
material_bought_val = pulp.value(material_bought)

output = {
    "dailyProfit": daily_profit,
    "unitsProduced": units_produced_vals,
    "overtimeAssembly": overtime_assembly_val,
    "materialBought": material_bought_val
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
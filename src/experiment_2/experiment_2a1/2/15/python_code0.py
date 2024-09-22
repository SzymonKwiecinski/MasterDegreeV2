import pulp
import json

data = {'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}

# Extract data for easier access
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
units_produced = [pulp.LpVariable(f'UnitsProduced_{i}', lowBound=0, cat='Integer') for i in range(N)]
overtime_assembly = pulp.LpVariable('OvertimeAssembly', lowBound=0, upBound=max_overtime_assembly)

# Objective function: Maximize daily profit
revenue = pulp.lpSum(prices[i] * units_produced[i] for i in range(N))
total_material_cost = pulp.lpSum(material_costs[i] * units_produced[i] for i in range(N))
effective_material_cost = total_material_cost * (1 - (material_discount / 100) * (total_material_cost > discount_threshold))

# Total assembly and testing hours
total_assembly_hours = pulp.lpSum(assembly_hours[i] * units_produced[i] for i in range(N)) + overtime_assembly
total_testing_hours = pulp.lpSum(testing_hours[i] * units_produced[i] for i in range(N))

# Constraints
problem += total_assembly_hours <= max_assembly + overtime_assembly
problem += total_testing_hours <= max_testing

# Objective function
profit = revenue - (effective_material_cost + overtime_assembly * overtime_assembly_cost)
problem += profit, "Total_Profit"

# Solve the problem
problem.solve()

# Retrieve results
daily_profit = pulp.value(problem.objective)
units_produced_values = [pulp.value(units_produced[i]) for i in range(N)]
overtime_assembly_value = pulp.value(overtime_assembly)
material_bought = sum(material_costs[i] * units_produced_values[i] for i in range(N))

# Output results
output = {
    "dailyProfit": daily_profit,
    "unitsProduced": units_produced_values,
    "overtimeAssembly": overtime_assembly_value,
    "materialBought": material_bought
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
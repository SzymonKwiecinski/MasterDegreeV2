import pulp
import json

data = {'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9],
        'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50,
        'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}

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

# Create the model
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
units_produced = pulp.LpVariable.dicts("UnitsProduced", range(N), lowBound=0, cat='Integer')
overtime_assembly = pulp.LpVariable("OvertimeAssembly", lowBound=0, upBound=max_overtime_assembly)

# Objective function
total_revenue = sum(prices[i] * units_produced[i] for i in range(N))
total_material_cost = sum(material_costs[i] * units_produced[i] for i in range(N))
total_overtime_cost = overtime_assembly * overtime_assembly_cost
total_cost = total_material_cost - (total_material_cost > discount_threshold) * (total_material_cost * material_discount) + total_overtime_cost

problem += total_revenue - total_cost, "Total_Profit"

# Constraints
problem += pulp.lpSum(assembly_hours[i] * units_produced[i] for i in range(N)) + overtime_assembly <= max_assembly, "Assembly_Limit"
problem += pulp.lpSum(testing_hours[i] * units_produced[i] for i in range(N)) <= max_testing, "Testing_Limit"

# Solve the problem
problem.solve()

# Collect results
daily_profit = pulp.value(problem.objective)
units_produced_result = [pulp.value(units_produced[i]) for i in range(N)]
overtime_assembly_result = pulp.value(overtime_assembly)
total_material_bought = sum(material_costs[i] * units_produced_result[i] for i in range(N))

# Print results
output = {
    "dailyProfit": daily_profit,
    "unitsProduced": units_produced_result,
    "overtimeAssembly": overtime_assembly_result,
    "materialBought": total_material_bought
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
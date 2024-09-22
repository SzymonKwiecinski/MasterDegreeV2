import pulp
import json

# Input data
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
material_cost = data['MaterialCost']
max_assembly = data['MaxAssembly']
max_testing = data['MaxTesting']
prices = data['Price']
max_overtime_assembly = data['MaxOvertimeAssembly']
overtime_assembly_cost = data['OvertimeAssemblyCost']
material_discount = data['MaterialDiscount']
discount_threshold = data['DiscountThreshold']

# Create the model
problem = pulp.LpProblem("ProfitMaximization", pulp.LpMaximize)

# Decision variables
units_produced = pulp.LpVariable.dicts("UnitsProduced", range(N), lowBound=0, cat='Integer')
overtime_assembly = pulp.LpVariable("OvertimeAssembly", lowBound=0, upBound=max_overtime_assembly)

# Objective function
total_revenue = pulp.lpSum(prices[i] * units_produced[i] for i in range(N))
total_material_cost = pulp.lpSum(material_cost[i] * units_produced[i] for i in range(N))
total_assembly_hour = pulp.lpSum(assembly_hours[i] * units_produced[i] for i in range(N))
total_testing_hour = pulp.lpSum(testing_hours[i] * units_produced[i] for i in range(N))

# Apply material discount
total_material_cost_discounted = total_material_cost * (1 - material_discount / 100) if total_material_cost > discount_threshold else total_material_cost

total_cost = total_material_cost_discounted + overtime_assembly * overtime_assembly_cost

problem += total_revenue - total_cost, "TotalProfit"

# Constraints
problem += total_assembly_hour + overtime_assembly <= max_assembly, "MaxAssemblyHours"
problem += total_testing_hour <= max_testing, "MaxTestingHours"

# Solve the problem
problem.solve()

# Collect results
daily_profit = pulp.value(problem.objective)
units_produced_values = [pulp.value(units_produced[i]) for i in range(N)]
overtime_assembly_value = pulp.value(overtime_assembly)
material_bought = pulp.value(total_material_cost)

# Output results
output = {
    "dailyProfit": daily_profit,
    "unitsProduced": units_produced_values,
    "overtimeAssembly": overtime_assembly_value,
    "materialBought": material_bought
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
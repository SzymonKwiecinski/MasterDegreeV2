import json
import pulp

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
material_discount = data['MaterialDiscount']
discount_threshold = data['DiscountThreshold']

# Create the linear programming problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
units_produced = [pulp.LpVariable(f'units_produced_{i}', lowBound=0, cat='Integer') for i in range(N)]
overtime_assembly = pulp.LpVariable('overtime_assembly', lowBound=0, upBound=max_overtime_assembly)

# Objective function
revenue = pulp.lpSum(prices[i] * units_produced[i] for i in range(N))
cost_of_materials = pulp.lpSum(material_costs[i] * units_produced[i] for i in range(N))
cost_of_overtime = overtime_assembly * overtime_assembly_cost
total_cost = cost_of_materials - (cost_of_materials * (material_discount / 100 if cost_of_materials > discount_threshold else 0))

problem += revenue - total_cost, "Total_Profit"

# Constraints
problem += pulp.lpSum(assembly_hours[i] * units_produced[i] for i in range(N)) + overtime_assembly <= max_assembly, "Assembly_Constraint"
problem += pulp.lpSum(testing_hours[i] * units_produced[i] for i in range(N)) <= max_testing, "Testing_Constraint"

# Solve the problem
problem.solve()

# Extract results
daily_profit = pulp.value(problem.objective)
units_produced_values = [pulp.value(units_produced[i]) for i in range(N)]
overtime_assembly_value = pulp.value(overtime_assembly)
material_bought = sum(material_costs[i] * units_produced_values[i] for i in range(N))

# Output results
result = {
    "dailyProfit": daily_profit,
    "unitsProduced": units_produced_values,
    "overtimeAssembly": overtime_assembly_value,
    "materialBought": material_bought
}

print(json.dumps(result))

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
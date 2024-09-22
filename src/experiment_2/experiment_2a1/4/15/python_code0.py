import json
import pulp

# Input data
data = {
    'N': 2,
    'AssemblyHour': [0.25, 0.3333],
    'TestingHour': [0.125, 0.3333],
    'MaterialCost': [1.2, 0.9],
    'MaxAssembly': 10,
    'MaxTesting': 70,
    'Price': [9, 8],
    'MaxOvertimeAssembly': 50,
    'OvertimeAssemblyCost': 5,
    'MaterialDiscount': 10,
    'DiscountThreshold': 300
}

# Extract the values from the data
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

# Create the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Create decision variables
units_produced = pulp.LpVariable.dicts("UnitsProduced", range(N), lowBound=0, cat='Integer')
overtime_assembly = pulp.LpVariable("OvertimeAssembly", lowBound=0)

# Objective function
revenue = pulp.lpSum([units_produced[i] * prices[i] for i in range(N)])
cost_material = pulp.lpSum([units_produced[i] * material_cost[i] for i in range(N)])
total_material_cost = cost_material * (1 - material_discount / 100) if cost_material > discount_threshold else cost_material
total_cost = total_material_cost + overtime_assembly * overtime_assembly_cost

problem += revenue - total_cost, "Total_Profit"

# Constraints
problem += pulp.lpSum([units_produced[i] * assembly_hours[i] for i in range(N)]) + overtime_assembly <= max_assembly, "Assembly_Hours_Constraint"
problem += pulp.lpSum([units_produced[i] * testing_hours[i] for i in range(N)]) <= max_testing, "Testing_Hours_Constraint"
problem += overtime_assembly <= max_overtime_assembly, "Max_Overtime_Assembly"

# Solve the problem
problem.solve()

# Output results
daily_profit = pulp.value(problem.objective)
units_produced_values = [units_produced[i].varValue for i in range(N)]
overtime_assembly_value = overtime_assembly.varValue
material_bought = sum(units_produced_values[i] * material_cost[i] for i in range(N))

# Print the objective value
print(f' (Objective Value): <OBJ>{daily_profit}</OBJ>')

# Prepare the output
output = {
    "dailyProfit": daily_profit,
    "unitsProduced": units_produced_values,
    "overtimeAssembly": overtime_assembly_value,
    "materialBought": material_bought
}

# Show the output
output
import pulp
import json

# Input data in JSON format
data = {'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 
        'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 
        'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 
        'MaterialDiscount': 10, 'DiscountThreshold': 300}

# Unpacking the data
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

# Defining the problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables for units produced of each product
units_produced = pulp.LpVariable.dicts("UnitsProduced", range(N), lowBound=0, cat='Integer')

# Decision variable for overtime assembly hours
overtime_assembly = pulp.LpVariable("OvertimeAssembly", lowBound=0, upBound=max_overtime_assembly)

# Objective function: Maximize profit
total_revenue = pulp.lpSum(price[i] * units_produced[i] for i in range(N))
total_material_cost = pulp.lpSum(material_cost[i] * units_produced[i] for i in range(N))
total_assembly_cost = overtime_assembly_cost * overtime_assembly
total_cost = total_material_cost + total_assembly_cost

# Effective material cost considering discount
effective_material_cost = total_material_cost * (1 - material_discount) if total_material_cost > discount_threshold else total_material_cost

profit = total_revenue - (effective_material_cost + total_assembly_cost)
problem += profit

# Constraints
problem += pulp.lpSum(assembly_hour[i] * units_produced[i] for i in range(N)) + overtime_assembly <= max_assembly
problem += pulp.lpSum(testing_hour[i] * units_produced[i] for i in range(N)) <= max_testing

# Solve the problem
problem.solve()

# Prepare the results
daily_profit = pulp.value(problem.objective)
units_produced_result = [pulp.value(units_produced[i]) for i in range(N)]
overtime_assembly_result = pulp.value(overtime_assembly)
material_cost_result = pulp.value(total_material_cost)

# Output results
output = {
    "dailyProfit": daily_profit,
    "unitsProduced": units_produced_result,
    "overtimeAssembly": overtime_assembly_result,
    "materialBought": material_cost_result
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
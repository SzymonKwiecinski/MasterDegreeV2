import pulp
import json

# Data input
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

# Variables
N = data['N']
assembly_hours = data['AssemblyHour']
testing_hours = data['TestingHour']
material_cost = data['MaterialCost']
max_assembly = data['MaxAssembly']
max_testing = data['MaxTesting']
prices = data['Price']
max_overtime = data['MaxOvertimeAssembly']
overtime_cost = data['OvertimeAssemblyCost']
material_discount = data['MaterialDiscount']
discount_threshold = data['DiscountThreshold']

# Create a problem variable
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables
units_produced = pulp.LpVariable.dicts("UnitsProduced", range(N), lowBound=0, cat='Integer')
overtime_assembly = pulp.LpVariable("OvertimeAssembly", lowBound=0, upBound=max_overtime, cat='Continuous')

# Objective Function
total_revenue = pulp.lpSum(prices[i] * units_produced[i] for i in range(N))
total_material_cost = pulp.lpSum(material_cost[i] * units_produced[i] for i in range(N))
total_testing_hours = pulp.lpSum(testing_hours[i] * units_produced[i] for i in range(N))
total_assembly_hours = pulp.lpSum(assembly_hours[i] * units_produced[i] for i in range(N))

# Calculate discounted material cost based on the total material cost
material_cost_after_discount = pulp.lpVariable("MaterialCostAfterDiscount")
problem += material_cost_after_discount == total_material_cost * (1 - (material_discount / 100)) * pulp.lpSum([1 if total_material_cost > discount_threshold else 0])
problem += material_cost_after_discount == total_material_cost * (1 if total_material_cost <= discount_threshold else 0)

# Profit Function
profit = total_revenue - (material_cost_after_discount + (overtime_assembly * overtime_cost))
problem += profit

# Constraints
problem += total_assembly_hours + overtime_assembly <= max_assembly
problem += total_testing_hours <= max_testing

# Solve the problem
problem.solve()

# Prepare results
daily_profit = pulp.value(problem.objective)
units_produced_result = [int(units_produced[i].varValue) for i in range(N)]
overtime_assembly_result = pulp.value(overtime_assembly)
material_bought_result = pulp.value(total_material_cost)

# Output results
output = {
    "dailyProfit": daily_profit,
    "unitsProduced": units_produced_result,
    "overtimeAssembly": overtime_assembly_result,
    "materialBought": material_bought_result
}

print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp
import json

# Given data in the specified JSON format
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

# Extracting parameters from the data
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

# Create the optimization problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision variables: units produced for each product and overtime hours
units_produced = [pulp.LpVariable(f'production_{i}', lowBound=0, cat='Integer') for i in range(N)]
overtime_assembly = pulp.LpVariable('overtime_assembly', lowBound=0, upBound=max_overtime_assembly, cat='Continuous')

# Objective function: maximize total profit
revenue = pulp.lpSum(prices[i] * units_produced[i] for i in range(N))
material_cost = pulp.lpSum(material_costs[i] * units_produced[i] for i in range(N))
total_material_cost = material_cost * (1 - material_discount) if material_cost > discount_threshold else material_cost
total_testing_cost = pulp.lpSum(testing_hours[i] * units_produced[i] for i in range(N))
total_assembly_cost = pulp.lpSum(assembly_hours[i] * units_produced[i] for i in range(N)) + overtime_assembly * overtime_assembly_cost

# Define profit objective
profit = revenue - (total_material_cost + total_testing_cost + total_assembly_cost)
problem += profit, "Total_Profit"

# Constraints
problem += pulp.lpSum(assembly_hours[i] * units_produced[i] for i in range(N)) + overtime_assembly <= max_assembly, "Assembly_Labor"
problem += pulp.lpSum(testing_hours[i] * units_produced[i] for i in range(N)) <= max_testing, "Testing_Labor"

# Solve the problem
problem.solve()

# Results
daily_profit = pulp.value(problem.objective)
units_produced_result = [pulp.value(units_produced[i]) for i in range(N)]
overtime_assembly_result = pulp.value(overtime_assembly)
material_bought = sum(pulp.value(units_produced[i]) * material_costs[i] for i in range(N))

# Output the results
output = {
    "dailyProfit": daily_profit,
    "unitsProduced": units_produced_result,
    "overtimeAssembly": overtime_assembly_result,
    "materialBought": material_bought
}

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')

# Return output (not part of the printing request but for completeness)
output
import pulp
import json

# Input data in JSON format
data = json.loads('{"N": 2, "AssemblyHour": [0.25, 0.3333], "TestingHour": [0.125, 0.3333], "MaterialCost": [1.2, 0.9], "MaxAssembly": 10, "MaxTesting": 70, "Price": [9, 8], "MaxOvertimeAssembly": 50, "OvertimeAssemblyCost": 5, "MaterialDiscount": 10, "DiscountThreshold": 300}')

# Extracting data
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

# Create the LP problem
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

# Decision variables
units_produced = [pulp.LpVariable(f'UnitsProduced_{i}', lowBound=0, cat='Integer') for i in range(N)]
overtime_assembly = pulp.LpVariable('OvertimeAssembly', lowBound=0, upBound=max_overtime_assembly)

# Objective function
revenue = pulp.lpSum([units_produced[i] * price[i] for i in range(N)])
material_cost_total = pulp.lpSum([units_produced[i] * material_cost[i] for i in range(N)])
# Apply discount if above threshold
material_cost_total_discounted = pulp.lpSum([units_produced[i] * material_cost[i] for i in range(N)]) * (1 - (material_discount / 100.0)) if pulp.lpSum([units_produced[i] * material_cost[i] for i in range(N)]) >= discount_threshold else pulp.lpSum([units_produced[i] * material_cost[i] for i in range(N)])

cost = material_cost_total_discounted + overtime_assembly * overtime_assembly_cost
profit = revenue - cost

problem += profit

# Constraints
problem += pulp.lpSum([units_produced[i] * assembly_hour[i] for i in range(N)]) + overtime_assembly <= max_assembly
problem += pulp.lpSum([units_produced[i] * testing_hour[i] for i in range(N)]) <= max_testing

# Solve the problem
problem.solve()

# Outputs
daily_profit = pulp.value(problem.objective)
units_produced_solution = [int(pulp.value(units_produced[i])) for i in range(N)]
overtime_assembly_solution = pulp.value(overtime_assembly)
material_bought = sum(units_produced_solution[i] * material_cost[i] for i in range(N))

# Print the results
output = {
    "dailyProfit": daily_profit,
    "unitsProduced": units_produced_solution,
    "overtimeAssembly": overtime_assembly_solution,
    "materialBought": material_bought
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
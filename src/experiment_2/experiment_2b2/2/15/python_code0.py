import pulp

# Extract data
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

# Initialize problem
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

# Decision variables
units_produced = [pulp.LpVariable(f"units_produced_{i}", lowBound=0, cat='Integer') for i in range(N)]
overtime_assembly = pulp.LpVariable("overtime_assembly", lowBound=0, upBound=max_overtime_assembly, cat='Continuous')

# Objective function
material_bought = sum(units_produced[i] * material_cost[i] for i in range(N))
material_final_cost = (1 if material_bought <= discount_threshold else 1 - material_discount / 100) * material_bought

profit = sum(units_produced[i] * prices[i] for i in range(N)) - material_final_cost - overtime_assembly * overtime_assembly_cost
problem += profit

# Constraints
problem += sum(units_produced[i] * assembly_hours[i] for i in range(N)) <= max_assembly + overtime_assembly
problem += sum(units_produced[i] * testing_hours[i] for i in range(N)) <= max_testing

# Solve problem
problem.solve()

# Results
daily_profit = pulp.value(profit)
units_result = [pulp.value(units_produced[i]) for i in range(N)]
overtime_assembly_result = pulp.value(overtime_assembly)
material_bought_result = pulp.value(material_bought)

output = {
    "dailyProfit": daily_profit,
    "unitsProduced": units_result,
    "overtimeAssembly": overtime_assembly_result,
    "materialBought": material_bought_result
}

print(output)
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
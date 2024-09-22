import pulp

# Data input
data = {
    "N": 2,
    "AssemblyHour": [0.25, 0.3333],
    "TestingHour": [0.125, 0.3333],
    "MaterialCost": [1.2, 0.9],
    "MaxAssembly": 10,
    "MaxTesting": 70,
    "Price": [9, 8],
    "MaxOvertimeAssembly": 50,
    "OvertimeAssemblyCost": 5,
    "MaterialDiscount": 10,
    "DiscountThreshold": 300
}

# Unpack data
N = data["N"]
assembly_hours = data["AssemblyHour"]
testing_hours = data["TestingHour"]
material_costs = data["MaterialCost"]
max_assembly = data["MaxAssembly"]
max_testing = data["MaxTesting"]
prices = data["Price"]
max_overtime_assembly = data["MaxOvertimeAssembly"]
overtime_assembly_cost = data["OvertimeAssemblyCost"]
material_discount = data["MaterialDiscount"]
discount_threshold = data["DiscountThreshold"]

# Create the problem
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

# Decision variables
units_produced = [pulp.LpVariable(f"unitsProduced_{i}", lowBound=0, cat='Integer') for i in range(N)]
overtime_assembly = pulp.LpVariable("overtimeAssembly", lowBound=0, cat='Continuous')
material_cost_discounted = pulp.LpVariable("materialCostDiscounted", lowBound=0)

# Constraints
# Assembly hours
assembly_constraint = sum(assembly_hours[i] * units_produced[i] for i in range(N)) <= max_assembly + overtime_assembly
problem += assembly_constraint

# Testing hours
testing_constraint = sum(testing_hours[i] * units_produced[i] for i in range(N)) <= max_testing
problem += testing_constraint

# Overtime assembly constraint
problem += overtime_assembly <= max_overtime_assembly

# Material cost and discount logic
material_cost = sum(material_costs[i] * units_produced[i] for i in range(N))
problem += material_cost_discounted == material_cost * (1 - material_discount / 100) * (material_cost >= discount_threshold) + material_cost * (material_cost < discount_threshold)

# Objective function
revenue = sum(prices[i] * units_produced[i] for i in range(N))
overtime_cost = overtime_assembly * overtime_assembly_cost
profit = revenue - material_cost_discounted - overtime_cost

problem += profit

# Solve the problem
problem.solve()

# Prepare the output
output = {
    "dailyProfit": pulp.value(profit),
    "unitsProduced": [pulp.value(units_produced[i]) for i in range(N)],
    "overtimeAssembly": pulp.value(overtime_assembly),
    "materialBought": sum(pulp.value(material_costs[i] * units_produced[i]) for i in range(N))
}

print(f" (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>")
print(output)
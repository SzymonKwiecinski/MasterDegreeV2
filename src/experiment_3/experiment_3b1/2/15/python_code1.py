import pulp
import json

# Data input
data = json.loads('{"N": 2, "AssemblyHour": [0.25, 0.3333], "TestingHour": [0.125, 0.3333], "MaterialCost": [1.2, 0.9], "MaxAssembly": 10, "MaxTesting": 70, "Price": [9, 8], "MaxOvertimeAssembly": 50, "OvertimeAssemblyCost": 5, "MaterialDiscount": 10, "DiscountThreshold": 300}')

# Parameters
N = data['N']
assemblyHour = data['AssemblyHour']
testingHour = data['TestingHour']
materialCost = data['MaterialCost']
maxAssembly = data['MaxAssembly']
maxTesting = data['MaxTesting']
price = data['Price']
maxOvertimeAssembly = data['MaxOvertimeAssembly']
overtimeAssemblyCost = data['OvertimeAssemblyCost']
materialDiscount = data['MaterialDiscount']
discountThreshold = data['DiscountThreshold']

# Problem Definition
problem = pulp.LpProblem("Production_Problem", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("UnitsProduced", range(N), lowBound=0, cat='Continuous')
overtimeAssembly = pulp.LpVariable("OvertimeAssembly", lowBound=0, cat='Continuous')

# Objective Function
profit_without_discount = pulp.lpSum(price[i] * x[i] for i in range(N)) - (
    pulp.lpSum(materialCost[i] * x[i] for i in range(N)) - 
    (materialDiscount / 100) * pulp.lpSum(materialCost[i] * x[i] for i in range(N)) * \
    pulp.lpSum(1 if pulp.lpSum(materialCost[i] * x[i] for i in range(N)) > discountThreshold else 0)
)
total_cost = pulp.lpSum(overtimeAssembly * overtimeAssemblyCost)
problem += profit_without_discount - total_cost, "Total_Profit"

# Constraints
problem += pulp.lpSum(assemblyHour[i] * x[i] for i in range(N)) + overtimeAssembly <= maxAssembly + maxOvertimeAssembly, "Assembly_Hours_Constraint"
problem += pulp.lpSum(testingHour[i] * x[i] for i in range(N)) <= maxTesting, "Testing_Hours_Constraint"

# Solve the problem
problem.solve()

# Output results
dailyProfit = pulp.value(problem.objective)
unitsProduced = {i: pulp.value(x[i]) for i in range(N)}
overtimeHoursScheduled = pulp.value(overtimeAssembly)
materialBought = sum(materialCost[i] * pulp.value(x[i]) for i in range(N))

print(f'(Objective Value): <OBJ>{dailyProfit}</OBJ>')
print(f'Units Produced: {unitsProduced}')
print(f'Overtime Assembly Hours Scheduled: {overtimeHoursScheduled}')
print(f'Total Material Bought: {materialBought}')
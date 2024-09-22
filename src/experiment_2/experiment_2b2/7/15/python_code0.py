import pulp
import json

# Input data
data = '''<DATA>
{'N': 2, 'AssemblyHour': [0.25, 0.3333], 'TestingHour': [0.125, 0.3333], 'MaterialCost': [1.2, 0.9], 'MaxAssembly': 10, 'MaxTesting': 70, 'Price': [9, 8], 'MaxOvertimeAssembly': 50, 'OvertimeAssemblyCost': 5, 'MaterialDiscount': 10, 'DiscountThreshold': 300}
</DATA>'''

data = json.loads(data)

# Variables
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

# Linear Program
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

# Decision Variables
unitsProduced = [pulp.LpVariable(f'UnitsProduced_{i}', lowBound=0, cat='Integer') for i in range(N)]
overtimeAssembly = pulp.LpVariable('OvertimeAssembly', lowBound=0, upBound=maxOvertimeAssembly, cat='Continuous')

# Objective: Maximize Profit
revenue = pulp.lpSum([price[i] * unitsProduced[i] for i in range(N)])
material_cost = pulp.lpSum([materialCost[i] * unitsProduced[i] for i in range(N)])
discount = pulp.LpVariable('Discount', lowBound=0, cat='Continuous')
cost = material_cost - discount + overtimeAssembly * overtimeAssemblyCost

problem += revenue - cost

# Constraints
# Assembly hours
problem += pulp.lpSum([assemblyHour[i] * unitsProduced[i] for i in range(N)]) + overtimeAssembly <= maxAssembly + maxOvertimeAssembly

# Testing hours
problem += pulp.lpSum([testingHour[i] * unitsProduced[i] for i in range(N)]) <= maxTesting

# Material discount condition
problem += discount <= materialDiscount / 100 * material_cost
problem += discount == 0 if material_cost <= discountThreshold else discount

# Solve the problem
problem.solve()

# Collect results
dailyProfit = pulp.value(problem.objective)
unitsProduced_result = [int(unitsProduced[i].varValue) for i in range(N)]
overtimeAssembly_result = overtimeAssembly.varValue
materialBought = sum(materialCost[i] * unitsProduced_result[i] for i in range(N))

# Output
output = {
    "dailyProfit": dailyProfit,
    "unitsProduced": unitsProduced_result,
    "overtimeAssembly": overtimeAssembly_result,
    "materialBought": materialBought
}

print(json.dumps(output, indent=4))
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
import pulp

# Data from JSON
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

# Number of products
N = data['N']

# Create the problem
problem = pulp.LpProblem("Maximize_Daily_Profit", pulp.LpMaximize)

# Decision variables
x = pulp.LpVariable.dicts("x", range(N), lowBound=0, cat='Integer')  # units of product i
o = pulp.LpVariable("o", lowBound=0)  # overtime hours

# Objective function
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(N)) - (
    pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(N)) * (1 - data['MaterialDiscount'] / 100) +
    data['OvertimeAssemblyCost'] * o
)
problem += profit

# Constraints
problem += pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(N)) + o <= data['MaxAssembly'] + data['MaxOvertimeAssembly'], "Assembly_Hours_Constraint"
problem += pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(N)) <= data['MaxTesting'], "Testing_Hours_Constraint"
problem += pulp.lpSum(data['MaterialCost'][i] * x[i] for i in range(N)) >= data['DiscountThreshold'], "Material_Cost_Constraint"

# Solve the problem
problem.solve()

# Output results
dailyProfit = pulp.value(problem.objective)
unitsProduced = [pulp.value(x[i]) for i in range(N)]
overtimeAssembly = pulp.value(o)
materialBought = sum(data['MaterialCost'][i] * unitsProduced[i] for i in range(N))

print(f' (Objective Value): <OBJ>{dailyProfit}</OBJ>')
print(f'Units Produced: {unitsProduced}')
print(f'Total Overtime Assembly Hours: {overtimeAssembly}')
print(f'Total Material Bought: {materialBought}')
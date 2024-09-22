import pulp
import json

# Data in JSON format
data = json.loads('{"N": 2, "AssemblyHour": [0.25, 0.3333], "TestingHour": [0.125, 0.3333], "MaterialCost": [1.2, 0.9], "MaxAssembly": 10, "MaxTesting": 70, "Price": [9, 8], "MaxOvertimeAssembly": 50, "OvertimeAssemblyCost": 5, "MaterialDiscount": 10, "DiscountThreshold": 300}')

# Define the problem
problem = pulp.LpProblem("Daily_Profit_Maximization", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(1, data['N'] + 1), lowBound=0, cat='Integer')
o = pulp.LpVariable("o", lowBound=0, cat='Integer')

# Total material cost
m = pulp.lpSum(data['MaterialCost'][i - 1] * x[i] for i in range(1, data['N'] + 1))

# Discount factor
delta = pulp.LpVariable("delta", lowBound=0)

# Objective Function
profit = pulp.lpSum(data['Price'][i - 1] * x[i] for i in range(1, data['N'] + 1)) - (m * (1 - delta)) - (o * data['OvertimeAssemblyCost'])
problem += profit, "Total Profit"

# Constraints
problem += pulp.lpSum(data['AssemblyHour'][i - 1] * x[i] for i in range(1, data['N'] + 1)) <= data['MaxAssembly'] + o, "AssemblyHours"
problem += pulp.lpSum(data['TestingHour'][i - 1] * x[i] for i in range(1, data['N'] + 1)) <= data['MaxTesting'], "TestingHours"
problem += o <= data['MaxOvertimeAssembly'], "MaxOvertime"

# Material discount constraint
problem += m <= data['DiscountThreshold'] + (1 - delta) * 1000, "MaterialDiscount"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')
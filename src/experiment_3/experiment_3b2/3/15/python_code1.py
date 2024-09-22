import pulp
import json

# Load data from JSON format
data = json.loads('{"N": 2, "AssemblyHour": [0.25, 0.3333], "TestingHour": [0.125, 0.3333], "MaterialCost": [1.2, 0.9], "MaxAssembly": 10, "MaxTesting": 70, "Price": [9, 8], "MaxOvertimeAssembly": 50, "OvertimeAssemblyCost": 5, "MaterialDiscount": 10, "DiscountThreshold": 300}')

# Define problem
problem = pulp.LpProblem("Maximize_Profit", pulp.LpMaximize)

# Decision Variables
x = pulp.LpVariable.dicts("x", range(data['N']), lowBound=0)  # Number of units of product produced
y = pulp.LpVariable("y", lowBound=0, upBound=data['MaxOvertimeAssembly'])  # Number of hours of overtime

# Objective Function
material_cost = pulp.lpSum((1 - data['MaterialDiscount'] / 100) * data['MaterialCost'][i] * x[i] if pulp.lpSum(data['MaterialCost'][j] * x[j] for j in range(data['N'])) > data['DiscountThreshold'] else data['MaterialCost'][i] * x[i] for i in range(data['N']))

overtime_cost = data['OvertimeAssemblyCost'] * y
profit = pulp.lpSum(data['Price'][i] * x[i] for i in range(data['N'])) - material_cost - overtime_cost

problem += profit

# Constraints
problem += pulp.lpSum(data['AssemblyHour'][i] * x[i] for i in range(data['N'])) + y <= data['MaxAssembly'] + data['MaxOvertimeAssembly'], "Assembly_Labor_Constraint"
problem += pulp.lpSum(data['TestingHour'][i] * x[i] for i in range(data['N'])) <= data['MaxTesting'], "Testing_Labor_Constraint"

# Solve the problem
problem.solve()

# Print the objective value
print(f' (Objective Value): <OBJ>{pulp.value(problem.objective)}</OBJ>')